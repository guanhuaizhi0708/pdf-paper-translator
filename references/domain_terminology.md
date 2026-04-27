# Sea Ice, Remote Sensing, and Deep Learning Terminology

Use this reference before translating papers about sea ice, polar remote sensing, SAR/PMW/optical products, and machine-learning retrieval. The glossary is a default baseline. If the paper, journal, or user's project provides an explicit preferred translation, follow that preference and keep it consistent.

## Translation Principles

1. Prefer established Chinese remote-sensing terminology over literal translations.
2. Translate geophysical variables precisely. Do not use everyday meanings when a domain term exists.
3. Keep sensor, mission, product, model, dataset, and algorithm names in English unless there is a widely used official Chinese name.
4. On first mention, write `中文术语（English Full Name, ABBR）` when the acronym matters. After that, use the acronym or Chinese term consistently.
5. If an English term is a product name or task label, keep it in English and add a Chinese descriptor only when helpful.
6. Do not translate proper nouns inside formulas, labels, file paths, citations, or code.

## High-Priority Conventions

| English | Preferred Chinese | Notes |
|---|---|---|
| sea ice | 海冰 | Not "海上冰". |
| sea ice concentration (SIC) | 海冰密集度（SIC） | Prefer "密集度" for the geophysical variable. If an existing document consistently uses "海冰浓度", keep consistency but avoid implying chemical concentration. |
| sea ice thickness (SIT) | 海冰厚度（SIT） |  |
| sea ice extent (SIE) | 海冰范围（SIE） | Usually area with SIC above a threshold, often 15%. |
| sea ice area (SIA) | 海冰面积（SIA） | Area-weighted SIC sum. Do not confuse with extent. |
| sea ice edge / ice edge | 海冰边缘 / 冰缘 | Use "冰缘" in specialist context. |
| marginal ice zone (MIZ) | 边缘冰区（MIZ） | Avoid "边际冰区" unless matching a prior project glossary. |
| open water | 开阔水域 | Not "开放水体". |
| lead | 冰隙 / 冰间水道 | Linear opening in sea ice. |
| polynya | 冰间湖 / 冰间水域 | Choose one and stay consistent; "冰间湖" is common. |
| melt pond | 融池 | Not "熔池". |
| melt pond fraction (MPF) | 融池比例 / 融池覆盖率（MPF） | Use "比例" for fractional variable; "覆盖率" when emphasizing surface coverage. |
| ice floe / floe | 浮冰块 | Avoid leaving "floe" untranslated in prose. |
| floe size | 浮冰块尺度 / 浮冰块大小 |  |
| stage of development (SoD) | 海冰发育阶段（SoD） | Ice chart attribute. |
| ice type | 冰型 / 海冰类型 |  |
| first-year ice (FYI) | 一年冰（FYI） |  |
| multiyear ice (MYI) | 多年冰（MYI） |  |
| young ice | 幼冰 / 年轻冰 | Use the paper's ice-stage convention if it follows WMO nomenclature. |
| new ice | 新生冰 |  |
| nilas | 尼拉斯冰 | Thin elastic ice crust. |
| pancake ice | 饼状冰 |  |
| fast ice | 固着冰 |  |
| drift ice / pack ice | 漂流冰 / 浮冰群 | Context-dependent. |
| ridging | 冰脊形成 / 起脊 |  |
| deformation | 形变 |  |
| freeboard | 干舷 | Sea ice or snow freeboard depending context. |
| draft | 吃水深度 | Sea-ice draft: 海冰吃水深度. |
| snow depth | 积雪深度 |  |
| snow density | 积雪密度 |  |

## Remote Sensing and Retrieval

| English | Preferred Chinese | Notes |
|---|---|---|
| remote sensing | 遥感 |  |
| retrieval | 反演 | Prefer "反演" for geophysical variables. Use "检索" only for information retrieval or when the paper explicitly means search/retrieval. |
| inversion | 反演 |  |
| forward model | 正演模型 |  |
| geophysical variable | 地球物理变量 |  |
| proxy variable | 代理变量 |  |
| reference product | 参考产品 | Do not call it ground truth unless it is true in situ truth. |
| ground truth | 真值 | Use carefully; many satellite products are only references. |
| validation | 验证 |  |
| calibration | 定标 / 校准 | "Radiometric calibration" -> 辐射定标. Model calibration -> 校准. |
| collocation | 时空匹配 / 配准匹配 | Use "时空匹配" for observation pairing. |
| coregistration / co-registration | 配准 |  |
| resampling | 重采样 |  |
| reprojection | 重投影 |  |
| gridding | 网格化 |  |
| swath | 刈幅 | SAR/PMW swath. |
| footprint | 足迹 | Sensor footprint. |
| pixel | 像元 | Prefer "像元" over "像素" for remote-sensing measurements. |
| grid cell | 网格单元 |  |
| spatial resolution | 空间分辨率 |  |
| temporal resolution | 时间分辨率 |  |
| revisit time | 重访周期 |  |
| incidence angle | 入射角 | SAR. |
| look angle | 视角 / 观测角 | Context-dependent. |
| azimuth direction | 方位向 |  |
| range direction | 距离向 |  |
| radiometer | 辐射计 |  |
| scatterometer | 散射计 |  |
| passive microwave (PMW) | 被动微波（PMW） |  |
| active microwave | 主动微波 |  |
| synthetic aperture radar (SAR) | 合成孔径雷达（SAR） |  |
| optical imagery | 光学影像 |  |
| infrared | 红外 |  |
| brightness temperature (TB) | 亮温（TB） | Not "亮度温度" unless source/project already uses it; "亮温" is standard. |
| backscatter | 后向散射 |  |
| backscatter coefficient | 后向散射系数 |  |
| normalized radar cross section (NRCS) | 归一化雷达截面（NRCS） | Often denoted `\sigma^0`; can also be described as 后向散射系数. |
| sigma nought / sigma zero (`\sigma^0`) | `\sigma^0` 后向散射系数 / 归一化雷达截面 | Keep formula unchanged. |
| polarization | 极化 |  |
| co-polarization | 同极化 |  |
| cross-polarization | 交叉极化 |  |
| HH/HV/VV/VH | HH/HV/VV/VH 极化 | Keep letter pairs unchanged. |
| speckle | 相干斑 | SAR noise texture. |
| thermal noise | 热噪声 |  |
| scalloping | 扇贝纹 / 扇贝效应 | SAR artifact; choose one and stay consistent. |
| noise vector | 噪声向量 | Sentinel-1 metadata. |
| denoising | 去噪 |  |
| radiometric bias | 辐射偏差 |  |
| land spillover | 陆地溢出 / 陆地信号溢出 | PMW coastal contamination. |
| atmospheric hydrometeors | 大气水凝物 |  |
| tie point | 系点 / 端元点 | For PMW sea-ice algorithms, "系点" is common. Add English on first mention. |
| weather filter | 天气滤波器 |  |
| ice mask | 海冰掩膜 |  |
| cloud mask | 云掩膜 |  |
| normalized difference snow index (NDSI) | 归一化差分积雪指数（NDSI） |  |
| near-infrared reflectance | 近红外反射率 |  |

## Sensors, Missions, Products, and Organizations

Keep these names in English; add Chinese descriptors only when useful.

| Name | Recommended Handling |
|---|---|
| Sentinel-1, Sentinel-2, Sentinel-3 | Keep English. Add "卫星/任务" if needed. |
| Landsat-8, OLI | Keep English; first mention can be "Operational Land Imager（OLI）". |
| AMSR2, SSMIS, SMMR, ESMR | Keep acronym; explain as radiometer/sensor if needed. |
| RADARSAT Constellation Mission (RCM) | Keep English with acronym RCM. |
| ROSE-L, CryoSat-2, ICESat-2, SMOS, SMAP | Keep English. |
| OSI SAF | Keep English; first mention "EUMETSAT Ocean and Sea Ice Satellite Application Facility（OSI SAF）". |
| NOAA/NSIDC | Keep English. |
| Copernicus Marine Service | Keep English or "哥白尼海洋服务（Copernicus Marine Service）" on first mention. |
| ESA, EUMETSAT, JAXA, NASA, DMI, NIC, CIS | Keep acronym; expand when paper does. |
| ice chart | 冰图 | National ice service product. |
| Level-1 / Level-2 / Level-3 (L1/L2/L3) | Level-1/Level-2/Level-3（L1/L2/L3）产品 | Keep level notation. |
| Ground Range Detected (GRD) | Ground Range Detected（GRD） | Sentinel-1 product type; do not translate acronym. |
| Extra Wide (EW) mode | Extra Wide（EW）模式 / 超宽幅（EW）模式 | Choose one; Sentinel-1 context often keeps EW English. |
| TOPSAR | TOPSAR 模式 |  |

## Deep Learning and Statistics

| English | Preferred Chinese | Notes |
|---|---|---|
| deep learning | 深度学习 |  |
| machine learning | 机器学习 |  |
| convolutional neural network (CNN) | 卷积神经网络（CNN） |  |
| ConvNet | ConvNet / 卷积网络 | Keep "ConvNet" if used as architecture shorthand. |
| UNet / U-Net | U-Net / UNet | Preserve the spelling used by the paper. |
| encoder | 编码器 |  |
| decoder | 解码器 |  |
| prediction head | 预测头 |  |
| multi-task learning | 多任务学习 |  |
| auxiliary task | 辅助任务 |  |
| knowledge distillation | 知识蒸馏 |  |
| teacher model | 教师模型 |  |
| student model | 学生模型 |  |
| ensemble | 集成模型 |  |
| soft target | 软目标 |  |
| logits | logits / 逻辑值 | Prefer "logits" in ML papers; explain once if needed. |
| softmax | softmax | Keep lowercase unless sentence start. |
| temperature scaling | 温度缩放 |  |
| cross-entropy loss | 交叉熵损失 |  |
| Kullback-Leibler divergence / KL divergence | Kullback-Leibler（KL）散度 / KL 散度 |  |
| loss function | 损失函数 |  |
| objective function | 目标函数 |  |
| training / validation / test set | 训练集 / 验证集 / 测试集 |  |
| train-validation-test split | 训练-验证-测试划分 |  |
| data augmentation | 数据增强 |  |
| random initialization | 随机初始化 |  |
| out-of-domain / out-of-distribution | 域外 / 分布外 | Pick by context. |
| generalization | 泛化能力 |  |
| uncertainty | 不确定性 |  |
| calibration (model) | 校准 |  |
| bias | 偏差 |  |
| variance | 方差 |  |
| standard deviation | 标准差 |  |
| root mean square error (RMSE) | 均方根误差（RMSE） |  |
| mean absolute error (MAE) | 平均绝对误差（MAE） |  |
| correlation coefficient | 相关系数 |  |
| Spearman rank correlation | Spearman 秩相关 |  |
| statistically significant | 统计显著 |  |
| p-value | p 值 |  |
| percentile | 百分位数 |  |
| confidence interval | 置信区间 |  |

## Common Bad Translations to Avoid

| Avoid | Prefer | Why |
|---|---|---|
| 海冰浓度 (when starting a new domain-consistent translation) | 海冰密集度 | SIC is a fractional coverage variable, not chemical concentration. |
| 检索海冰浓度 | 反演海冰密集度 | Remote-sensing retrieval of geophysical variables is normally "反演". |
| 亮度温度 | 亮温 | "亮温" is the standard remote-sensing term. |
| 像素 (for gridded remote-sensing measurements) | 像元 | "像元" is more precise in remote sensing. |
| 边际冰区 | 边缘冰区 | More natural specialist term for MIZ. |
| 漂浮物大小 / 浮冰大小 (ambiguous) | 浮冰块尺度 | For floe size. |
| 被动微波基础产品 | 基于被动微波的产品 | Better Chinese syntax. |
| 地面真值 (for another satellite product) | 参考产品 / 参考数据 | Avoid overclaiming ground truth. |
| 代理 (for agent in AI) | 智能体 | AI papers. |
| 管线 | 流程 / 处理流程 | "Pipeline" in methods is usually "流程". |

## Term-Building Procedure for Each Paper

Before translating:

1. Read title, abstract, section headings, captions, and method paragraphs.
2. Extract candidate terms in these groups:
   - target variables: SIC, SIT, SIA, SIE, MPF, freeboard, snow depth
   - sensors/products: Sentinel-1, AMSR2, OSI SAF, NOAA/NSIDC, Landsat-8
   - signal terms: brightness temperature, backscatter, polarization, incidence angle
   - method terms: retrieval, calibration, resampling, U-Net, distillation, loss
   - evaluation terms: RMSE, bias, correlation, validation, reference product
3. Merge candidates with this glossary. The glossary wins unless the paper/user has a clear convention.
4. Add paper-specific names as `(保留)`, for example `DMI-ASIP → (保留)`.
5. Use the same terminology table for all files/sections in the paper.

## Review Checklist

- [ ] `sea ice concentration` is translated consistently as `海冰密集度` unless a project-specific choice is documented.
- [ ] `retrieval` and `inversion` are translated as `反演` in geophysical contexts.
- [ ] `brightness temperature` is translated as `亮温`.
- [ ] `backscatter` and `\sigma^0` are translated with SAR terminology.
- [ ] `sea ice area` and `sea ice extent` are not confused.
- [ ] Product/sensor/dataset names remain in English with acronyms preserved.
- [ ] Reference products are not called `真值` unless they are true in situ ground truth.
- [ ] Deep-learning terms are consistent across method, table, and caption text.
