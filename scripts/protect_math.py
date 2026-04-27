#!/usr/bin/env python3
"""Protect, restore, and validate Markdown math during paper translation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"@@MATH_(\d{6})@@")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
MACRO_CJK_RE = re.compile(r"\\[A-Za-z]+[\u3400-\u4dbf\u4e00-\u9fff]")


@dataclass
class MathToken:
    text: str
    line: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def split_fenced_code(text: str) -> list[tuple[bool, str]]:
    """Return (is_code, segment) pairs, keeping fenced blocks untouched."""
    parts: list[tuple[bool, str]] = []
    buffer: list[str] = []
    in_fence = False
    fence_marker = ""

    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        starts_fence = stripped.startswith("```") or stripped.startswith("~~~")
        marker = stripped[:3] if starts_fence else ""

        if starts_fence and not in_fence:
            if buffer:
                parts.append((False, "".join(buffer)))
                buffer = []
            in_fence = True
            fence_marker = marker
            buffer.append(line)
            continue

        if starts_fence and in_fence and marker == fence_marker:
            buffer.append(line)
            parts.append((True, "".join(buffer)))
            buffer = []
            in_fence = False
            fence_marker = ""
            continue

        buffer.append(line)

    if buffer:
        parts.append((in_fence, "".join(buffer)))
    return parts


def find_unescaped(text: str, needle: str, start: int) -> int:
    cursor = start
    while True:
        index = text.find(needle, cursor)
        if index == -1:
            return -1
        if not is_escaped(text, index):
            return index
        cursor = index + len(needle)


def extract_math_from_segment(
    segment: str, line_offset: int = 0
) -> tuple[list[MathToken], list[str]]:
    tokens: list[MathToken] = []
    errors: list[str] = []
    i = 0

    while i < len(segment):
        if segment.startswith("$$", i) and not is_escaped(segment, i):
            end = find_unescaped(segment, "$$", i + 2)
            line = line_offset + segment.count("\n", 0, i) + 1
            if end == -1:
                errors.append(f"line {line}: unclosed display math delimiter $$")
                i += 2
                continue
            tokens.append(MathToken(segment[i : end + 2], line))
            i = end + 2
            continue

        if segment.startswith("\\[", i) and not is_escaped(segment, i):
            end = find_unescaped(segment, "\\]", i + 2)
            line = line_offset + segment.count("\n", 0, i) + 1
            if end == -1:
                errors.append(f"line {line}: unclosed display math delimiter \\[")
                i += 2
                continue
            tokens.append(MathToken(segment[i : end + 2], line))
            i = end + 2
            continue

        if segment.startswith("\\(", i) and not is_escaped(segment, i):
            end = find_unescaped(segment, "\\)", i + 2)
            line = line_offset + segment.count("\n", 0, i) + 1
            if end == -1:
                errors.append(f"line {line}: unclosed inline math delimiter \\(")
                i += 2
                continue
            tokens.append(MathToken(segment[i : end + 2], line))
            i = end + 2
            continue

        if segment[i] == "$" and not is_escaped(segment, i):
            if segment.startswith("$$", i):
                i += 1
                continue
            cursor = i + 1
            end = -1
            while cursor < len(segment):
                if (
                    segment[cursor] == "$"
                    and not is_escaped(segment, cursor)
                    and not segment.startswith("$$", cursor)
                ):
                    end = cursor
                    break
                cursor += 1
            line = line_offset + segment.count("\n", 0, i) + 1
            if end == -1:
                errors.append(f"line {line}: unclosed inline math delimiter $")
                i += 1
                continue
            tokens.append(MathToken(segment[i : end + 1], line))
            i = end + 1
            continue

        i += 1

    return tokens, errors


def extract_math(text: str) -> tuple[list[MathToken], list[str]]:
    tokens: list[MathToken] = []
    errors: list[str] = []
    line_offset = 0
    for is_code, segment in split_fenced_code(text):
        if not is_code:
            segment_tokens, segment_errors = extract_math_from_segment(segment, line_offset)
            tokens.extend(segment_tokens)
            errors.extend(segment_errors)
        line_offset += segment.count("\n")
    return tokens, errors


def replace_math_in_segment(
    segment: str, counter_start: int
) -> tuple[str, list[dict[str, str]], int]:
    pieces: list[str] = []
    items: list[dict[str, str]] = []
    i = 0
    counter = counter_start

    def emit_math(end: int) -> None:
        nonlocal i, counter
        placeholder = f"@@MATH_{counter:06d}@@"
        math_text = segment[i:end]
        line = segment.count("\n", 0, i) + 1
        pieces.append(placeholder)
        items.append({"placeholder": placeholder, "math": math_text, "line": line})
        counter += 1
        i = end

    while i < len(segment):
        if segment.startswith("$$", i) and not is_escaped(segment, i):
            end = find_unescaped(segment, "$$", i + 2)
            if end != -1:
                emit_math(end + 2)
                continue

        if segment.startswith("\\[", i) and not is_escaped(segment, i):
            end = find_unescaped(segment, "\\]", i + 2)
            if end != -1:
                emit_math(end + 2)
                continue

        if segment.startswith("\\(", i) and not is_escaped(segment, i):
            end = find_unescaped(segment, "\\)", i + 2)
            if end != -1:
                emit_math(end + 2)
                continue

        if segment[i] == "$" and not is_escaped(segment, i) and not segment.startswith("$$", i):
            cursor = i + 1
            end = -1
            while cursor < len(segment):
                if (
                    segment[cursor] == "$"
                    and not is_escaped(segment, cursor)
                    and not segment.startswith("$$", cursor)
                ):
                    end = cursor
                    break
                cursor += 1
            if end != -1:
                emit_math(end + 1)
                continue

        pieces.append(segment[i])
        i += 1

    return "".join(pieces), items, counter


def protect_markdown(input_path: Path, output_path: Path, manifest_path: Path) -> int:
    text = read_text(input_path)
    output_parts: list[str] = []
    all_items: list[dict[str, str]] = []
    counter = 1
    line_offset = 0

    for is_code, segment in split_fenced_code(text):
        if is_code:
            output_parts.append(segment)
        else:
            protected, items, counter = replace_math_in_segment(segment, counter)
            for item in items:
                item["line"] = str(int(item["line"]) + line_offset)
            all_items.extend(items)
            output_parts.append(protected)
        line_offset += segment.count("\n")

    manifest = {
        "version": 1,
        "source": str(input_path),
        "count": len(all_items),
        "items": all_items,
    }
    write_text(output_path, "".join(output_parts))
    write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"Protected {len(all_items)} math spans -> {output_path}")
    print(f"Wrote manifest -> {manifest_path}")
    return 0


def restore_markdown(input_path: Path, output_path: Path, manifest_path: Path) -> int:
    text = read_text(input_path)
    manifest = json.loads(read_text(manifest_path))
    missing: list[str] = []

    for item in manifest["items"]:
        placeholder = item["placeholder"]
        if placeholder not in text:
            missing.append(placeholder)
            continue
        text = text.replace(placeholder, item["math"])

    if missing:
        for placeholder in missing[:20]:
            print(f"ERROR: missing placeholder {placeholder}", file=sys.stderr)
        if len(missing) > 20:
            print(f"ERROR: ... and {len(missing) - 20} more", file=sys.stderr)
        return 1

    leftovers = sorted(set(match.group(0) for match in PLACEHOLDER_RE.finditer(text)))
    if leftovers:
        for placeholder in leftovers[:20]:
            print(f"ERROR: leftover placeholder {placeholder}", file=sys.stderr)
        return 1

    write_text(output_path, text)
    print(f"Restored {manifest['count']} math spans -> {output_path}")
    return 0


def has_unescaped_percent(math_text: str) -> bool:
    return any(ch == "%" and not is_escaped(math_text, index) for index, ch in enumerate(math_text))


def validate_markdown(path: Path, strict_cjk: bool = False) -> int:
    text = read_text(path)
    tokens, parse_errors = extract_math(text)
    errors = list(parse_errors)
    warnings: list[str] = []

    if "\ufffd" in text:
        errors.append("file contains U+FFFD replacement characters")

    placeholders = sorted(set(match.group(0) for match in PLACEHOLDER_RE.finditer(text)))
    if placeholders:
        errors.append(f"file still contains math placeholders: {', '.join(placeholders[:10])}")

    for token in tokens:
        if has_unescaped_percent(token.text):
            errors.append(f"line {token.line}: unescaped % inside math; use \\%")
        if MACRO_CJK_RE.search(token.text):
            errors.append(f"line {token.line}: LaTeX command is directly followed by CJK text")
        if CJK_RE.search(token.text):
            message = f"line {token.line}: CJK character appears inside math"
            if strict_cjk:
                errors.append(message)
            else:
                warnings.append(message)

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        return 1

    print(f"Checked {path}: {len(tokens)} math spans, {len(warnings)} warnings, 0 errors")
    return 0


def compare_math(source_path: Path, translated_path: Path) -> int:
    source_text = read_text(source_path)
    translated_text = read_text(translated_path)
    source_tokens, source_errors = extract_math(source_text)
    translated_tokens, translated_errors = extract_math(translated_text)
    errors = [f"source: {error}" for error in source_errors]
    errors.extend(f"translated: {error}" for error in translated_errors)

    if len(source_tokens) != len(translated_tokens):
        errors.append(
            f"math span count differs: source={len(source_tokens)} translated={len(translated_tokens)}"
        )

    for index, (source, translated) in enumerate(zip(source_tokens, translated_tokens), start=1):
        if source.text != translated.text:
            errors.append(
                "math span differs at index "
                f"{index} (source line {source.line}, translated line {translated.line})\n"
                f"  source: {source.text}\n"
                f"  translated: {translated.text}"
            )
            if len(errors) >= 10:
                break

    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        return 1

    print(f"Math compare passed: {len(source_tokens)} spans unchanged")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    protect_parser = subparsers.add_parser("protect", help="replace Markdown math with placeholders")
    protect_parser.add_argument("input", type=Path)
    protect_parser.add_argument("--output", required=True, type=Path)
    protect_parser.add_argument("--manifest", required=True, type=Path)

    restore_parser = subparsers.add_parser("restore", help="restore placeholders from a manifest")
    restore_parser.add_argument("input", type=Path)
    restore_parser.add_argument("--output", required=True, type=Path)
    restore_parser.add_argument("--manifest", required=True, type=Path)

    check_parser = subparsers.add_parser("check", help="validate Markdown math delimiters/content")
    check_parser.add_argument("input", type=Path)
    check_parser.add_argument("--strict-cjk", action="store_true")

    compare_parser = subparsers.add_parser("compare", help="verify math is unchanged between files")
    compare_parser.add_argument("source", type=Path)
    compare_parser.add_argument("translated", type=Path)

    args = parser.parse_args(argv)
    if args.command == "protect":
        return protect_markdown(args.input, args.output, args.manifest)
    if args.command == "restore":
        return restore_markdown(args.input, args.output, args.manifest)
    if args.command == "check":
        return validate_markdown(args.input, args.strict_cjk)
    if args.command == "compare":
        return compare_math(args.source, args.translated)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
