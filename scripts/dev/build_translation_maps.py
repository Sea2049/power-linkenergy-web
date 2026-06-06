"""Build zh/fr/ru translation map JSON files from English strings."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRINGS_FILE = ROOT / "assets" / "locales" / "_strings.txt"
OUT_DIR = ROOT / "scripts" / "translation_maps"


def zh_map() -> dict[str, str]:
    return {
        "01": "01", "02": "02", "03": "03", "04": "04",
        "Home": "首页", "Solutions": "解决方案", "Products": "产品", "Reference Frameworks": "参考框架",
        "About Us": "关于我们", "Contact": "联系我们",
        "Integrated Power Solutions for Critical Applications": "关键应用一体化电源解决方案",
        "Powerlink Energy integrated power solutions for critical applications": "Powerlink Energy 关键应用一体化电源解决方案",
        "Data Centers": "数据中心", "Telecom Sites": "通信站点", "Commercial & Industrial Energy Storage": "工商业储能",
        "Residential Solar Storage": "户用光储", "Edge Computing": "边缘计算", "Safety Monitoring Applications": "安全监控应用",
        "Flexible MOQ": "灵活起订量",
        "We support practical order quantities for small-batch supply, pilot projects, and phased purchasing.": "我们支持小批量供货、试点项目和分阶段采购的务实起订量。",
        "Fast Solution Matching": "快速方案匹配",
        "We focus on quick communication and practical configuration support based on the application, power requirement, and target market.": "我们根据应用场景、功率需求和目标市场，专注于快速沟通与务实的配置支持。",
        "One-Stop Integration": "一站式集成",
        "We help combine power hosts, batteries, DC/DC modules, industrial cabling, and monitoring accessories into complete solution packages.": "我们帮助将电源主机、电池、DC/DC 模块、工业线缆和监控配件组合为完整方案包。",
        "Responsive Support": "快速响应支持",
        "We value efficient communication and practical support throughout product selection, quotation, and project follow-up.": "我们重视在产品选型、报价和项目跟进全流程中的高效沟通与务实支持。",
        "Powerlink Energy provides UPS systems, energy storage solutions, telecom power equipment, DC/DC modules, industrial cabling, and monitoring accessories for data centers, telecom sites, commercial energy storage, and other demanding environments.": "Powerlink Energy 为数据中心、通信站点、工商业储能及其他严苛环境提供 UPS 系统、储能方案、通信电源设备、DC/DC 模块、工业线缆及监控配件。",
        "Commercial energy storage and integrated power equipment": "工商业储能及一体化电源设备",
        "Integrated telecom and backup power equipment for project inquiries": "用于项目咨询的一体化通信与备用电源设备",
        "Data Center Backup Power": "数据中心备用电源",
        "Reliable backup power solutions for small and medium-sized server rooms, IDC facilities, and network cabinets.": "为中小型机房、IDC 设施及网络机柜提供可靠的备用电源解决方案。",
        "Data center and backup power equipment environment": "数据中心与备用电源设备环境",
        "This solution focuses on reliable backup power continuity for server rooms, network cabinets, and compact data center deployments where uptime matters.": "本方案聚焦机房、网络机柜及紧凑型数据中心部署中对运行连续性要求较高的可靠备用电源保障。",
        "Maintain stable output during utility instability or outages.": "在市电波动或停电期间保持稳定输出。",
        "Fit backup equipment into limited technical room space.": "在有限的技术机房空间内部署备用设备。",
        "Balance runtime, battery footprint, and project budget.": "在备电时长、电池占地与项目预算之间取得平衡。",
        "Online UPS host sized to the target IT load.": "按目标 IT 负载选型的在线式 UPS 主机。",
        "Lithium or VRLA battery bank for the required backup duration.": "满足所需备电时长的锂电或 VRLA 电池组。",
        "Input and output distribution accessories with monitoring support.": "带监控支持的输入输出配电附件。",
        "Improves power continuity for critical IT equipment.": "提升关键 IT 设备的供电连续性。",
        "Supports phased scaling for growing server loads.": "支持随服务器负载增长的分阶段扩容。",
        "Simplifies sourcing with matched core equipment and accessories.": "通过匹配核心设备与配件简化采购。",
        "We help clarify runtime targets, power range, installation constraints, and delivery scope before quotation.": "我们在报价前协助明确备电时长目标、功率范围、安装约束及交付范围。",
        "Telecom Base Station Backup Power": "通信基站备用电源",
        "Integrated backup power for telecom towers and remote communication sites with stable performance and flexible configuration.": "为通信塔及偏远通信站点提供性能稳定、配置灵活的集成备用电源。",
        "Telecom and UPS power equipment": "通信与 UPS 电源设备",
        "This package supports distributed telecom sites that need dependable backup power, compact footprints, and straightforward maintenance.": "本方案适用于需要可靠备用电源、紧凑占地和简便维护的分布式通信站点。",
        "Remote sites need high reliability with limited on-site service.": "偏远站点在有限现场服务条件下仍需高可靠性。",
        "Projects often require practical combinations of rectifiers, batteries, and accessories.": "项目通常需要整流器、电池与配件的务实组合。",
        "Environmental and deployment differences increase configuration complexity.": "环境与部署差异增加了配置复杂度。",
        "Telecom rectifier or UPS main power unit.": "通信整流器或 UPS 主电源单元。",
        "Battery bank matched to site autonomy requirements.": "按站点自主供电需求匹配的电池组。",
        "Monitoring modules, breakers, and cabling for field integration.": "用于现场集成的监控模块、断路器及线缆。",
        "Provides a practical supply path for telecom power projects.": "为通信电源项目提供务实的供货路径。",
        "Supports distributed deployment across multiple station types.": "支持多种站型的分布式部署。",
        "Keeps configuration aligned with target runtime and site conditions.": "使配置与目标备电时长及站点条件保持一致。",
        "We help match product scope around station type, load profile, runtime target, and market requirement.": "我们根据站型、负载特性、备电目标及市场需求协助匹配产品范围。",
        "Practical storage solutions for peak shaving, backup power, and energy management in commercial and industrial environments.": "面向工商业场景的削峰填谷、备用电源及能源管理务实储能方案。",
        "Commercial and industrial energy storage equipment": "工商业储能设备",
        "This solution targets site-level storage use cases such as peak shaving, time-of-use optimization, and backup support for commercial and industrial facilities.": "本方案面向站点级储能应用，如削峰填谷、分时电价优化及工商业设施的备用支持。",
        "Projects need a workable combination of storage, inverter, and protection devices.": "项目需要储能、逆变器与保护装置的可行组合。",
        "Site objectives vary between backup, arbitrage, and energy optimization.": "站点目标在备用、套利与能源优化之间各不相同。",
        "Customers need a configuration path that is clear before deeper engineering.": "客户需要在深入工程设计前获得清晰的配置路径。",
        "Battery storage rack or cabinet.": "电池储能机架或机柜。",
        "Hybrid or PCS inverter matched to the application profile.": "按应用特性匹配的混合逆变器或 PCS。",
        "Monitoring, distribution, and safety accessories for site integration.": "用于站点集成的监控、配电及安全附件。",
        "Supports practical storage deployment discussions early in the sales cycle.": "在销售周期早期支持务实的储能部署讨论。",
        "Helps structure product matching around real site goals.": "围绕真实站点目标构建产品匹配结构。",
        "Makes later engineering handoff easier with a clearer product scope.": "通过更清晰的产品范围简化后续工程交接。",
        "We align storage direction with application goals, installation conditions, and expected delivery scope.": "我们根据应用目标、安装条件及预期交付范围对齐储能方向。",
        "Hybrid solar and battery solutions for homes and small offices requiring stable power and backup capability.": "为家庭及小型办公场所提供稳定供电与备用能力的光储混合方案。",
        "Hybrid inverter and battery storage setup": "混合逆变器与电池储能配置",
        "This package is designed for home and light commercial users who need solar-linked storage, backup capability, and simple deployment logic.": "本方案面向需要光伏联动储能、备用能力及简便部署逻辑的户用与轻商用用户。",
        "Different homes require different balances between backup, self-consumption, and budget.": "不同家庭在备用、自发自用与预算之间需要不同平衡。",
        "Users want simpler product combinations instead of fragmented category selection.": "用户希望获得更简单的产品组合，而非零散的品类选择。",
        "Installers need a clear hardware scope for quotation and planning.": "安装商需要清晰的硬件范围以便报价与规划。",
        "Hybrid inverter or solar inverter.": "混合逆变器或光伏逆变器。",
        "Lithium battery pack matched to backup and energy goals.": "按备用与用能目标匹配的锂电池组。",
        "Basic accessories and monitoring for safe operation.": "保障安全运行的基础配件与监控。",
        "Helps combine inverter and storage selection into one path.": "将逆变器与储能选型整合为一条路径。",
        "Supports residential backup and self-consumption discussions.": "支持户用备用与自发自用相关讨论。",
        "Fits projects that need practical, entry-friendly configuration.": "适用于需要务实、易上手配置的项目。",
        "We help match inverter and storage direction based on backup need, daily usage, and installation scenario.": "我们根据备用需求、日常用电及安装场景协助匹配逆变器与储能方向。",
        "Edge Computing Power": "边缘计算电源",
        "Compact and efficient power systems for edge nodes, distributed IT loads, and space-limited installations.": "面向边缘节点、分布式 IT 负载及空间受限安装的紧凑高效电源系统。",
        "Compact power equipment for distributed IT loads": "分布式 IT 负载紧凑电源设备",
        "This scenario serves distributed IT environments where compact backup power and reliable operation are needed close to the load.": "本场景适用于需要在负载近端提供紧凑备用电源与可靠运行的分布式 IT 环境。",
        "Edge sites often have limited rack or cabinet space.": "边缘站点通常机架或机柜空间有限。",
        "Power support still needs continuity despite small deployment scale.": "即便部署规模较小，供电仍需保持连续性。",
        "Projects benefit from compact, integration-ready hardware combinations.": "项目受益于紧凑、可快速集成的硬件组合。",
        "Compact UPS host or distributed backup module.": "紧凑型 UPS 主机或分布式备用模块。",
        "Battery pack sized for short to medium runtime support.": "按短至中等备电时长配置的电池组。",
        "Monitoring and connection accessories for fast deployment.": "用于快速部署的监控与连接附件。",
        "Supports distributed power continuity for edge nodes.": "支持边缘节点的分布式供电连续性。",
        "Keeps equipment footprint aligned with compact environments.": "使设备占地与紧凑环境相匹配。",
        "Simplifies sourcing for small but power-sensitive deployments.": "简化小规模但对供电敏感部署的采购。",
        "We help evaluate footprint, runtime, and environment constraints before final category matching.": "我们在最终品类匹配前协助评估占地、备电时长及环境约束。",
        "Safety Monitoring Solutions": "安全监控解决方案",
        "Monitoring-oriented solution packages for temperature sensing, environmental supervision, and safety-related applications.": "面向温度传感、环境监管及安全相关应用的监控型方案包。",
        "Power monitoring and industrial supervision equipment": "电力监控与工业监管设备",
        "This solution focuses on monitoring accessories and supporting power elements for safety supervision, sensing, and environmental alert scenarios.": "本方案聚焦安全监管、传感及环境告警场景中的监控配件与配套电源要素。",
        "Projects often need both power support and sensing accessories.": "项目通常同时需要供电支持与传感配件。",
        "Different monitoring environments require different combinations of probes, cabling, and integration items.": "不同监控环境需要不同的探头、线缆及集成件组合。",
        "Customers want a practical list that goes beyond a single product SKU.": "客户希望获得超越单一 SKU 的务实清单。",
        "Monitoring host or power support equipment.": "监控主机或供电支持设备。",
        "Sensors, probes, or field accessories matched to the environment.": "按环境匹配的传感器、探头或现场配件。",
        "Industrial cabling and connection parts for deployment.": "用于部署的工业线缆与连接件。",
        "Links sensing accessories with the surrounding power context.": "将传感配件与周边供电环境相关联。",
        "Supports clearer project communication for monitoring applications.": "支持监控应用项目中更清晰的沟通。",
        "Improves category completeness for safety-oriented sourcing.": "提升面向安全场景的采购品类完整性。",
        "We help define the application environment, accessory scope, and integration priorities before quotation.": "我们在报价前协助界定应用环境、配件范围及集成优先级。",
        "UPS Systems": "UPS 系统",
        "Backup power systems for IT, telecom, edge, and industrial applications that require stable power continuity.": "面向需要稳定供电连续性的 IT、通信、边缘及工业应用的备用电源系统。",
        "UPS backup power equipment": "UPS 备用电源设备",
        "UPS systems remain a core category for customers who need stable backup continuity across IT, telecom, and industrial use cases.": "UPS 系统是客户在 IT、通信及工业场景中实现稳定备用连续性的核心品类。",
        "Server rooms and data cabinets": "机房与数据机柜",
        "Telecom and distributed communications": "通信与分布式通信",
        "Industrial control and edge environments": "工业控制与边缘环境",
        "Online UPS units": "在线式 UPS 主机",
        "Rack and tower form factors": "机架式与塔式结构",
        "Battery expansion and accessory options": "电池扩展及配件选项",
        "Supports stable backup continuity.": "支持稳定的备用连续性。",
        "Fits multiple deployment scales.": "适配多种部署规模。",
        "Works well as part of integrated project packages.": "可作为集成项目方案包的重要组成部分。",
        "Lithium Battery Systems": "锂电池系统",
        "Lithium battery storage systems for backup power, telecom, and energy storage projects requiring practical integration.": "面向备用电源、通信及储能项目、需要务实集成的锂电池储能系统。",
        "Lithium battery storage system equipment": "锂电池储能系统设备",
        "Lithium battery systems support backup, storage, and telecom applications that need practical runtime planning and flexible system matching.": "锂电池系统支持需要务实备电规划与灵活系统匹配的备用、储能及通信应用。",
        "UPS runtime expansion": "UPS 备电时长扩展",
        "Telecom backup power": "通信备用电源",
        "Energy storage support projects": "储能配套项目",
        "Rack battery modules": "机架电池模块",
        "Cabinet-level storage options": "机柜级储能选项",
        "Battery management related components": "电池管理相关组件",
        "Improves energy density for many projects.": "提升众多项目的能量密度。",
        "Supports integrated backup and storage discussions.": "支持集成备用与储能相关讨论。",
        "Works with phased and scalable configurations.": "支持分阶段与可扩展配置。",
        "Hybrid / Solar Inverters": "混合/光伏逆变器",
        "Hybrid and solar inverter categories for residential, commercial, and storage-linked power conversion applications.": "面向户用、商用及储能联动电能转换应用的混合与光伏逆变器品类。",
        "Hybrid inverter and solar storage equipment": "混合逆变器与光储设备",
        "This category supports solar and hybrid projects that require conversion equipment matched to storage or grid-linked application goals.": "本品类支持需要与储能或并网应用目标匹配的转换设备的光伏与混合项目。",
        "Small commercial backup and self-consumption": "小型商用备用与自发自用",
        "Energy-linked conversion projects": "能源联动转换项目",
        "Hybrid inverter units": "混合逆变器单元",
        "Solar inverter variants": "光伏逆变器型号",
        "Accessory and monitoring support items": "配件与监控支持件",
        "Helps combine conversion and storage planning.": "有助于整合转换与储能规划。",
        "Supports practical category selection before system engineering.": "在系统工程前支持务实的品类选择。",
        "Fits both residential and light commercial discussions.": "适用于户用与轻商用场景讨论。",
        "Telecom & DC Power": "通信与直流电源",
        "Telecom power equipment and DC support modules for distributed communication sites and industrial power applications.": "面向分布式通信站点及工业电源应用的通信电源设备与直流支持模块。",
        "Telecom and DC power equipment": "通信与直流电源设备",
        "This category covers telecom power equipment and DC support modules for distributed sites and related project environments.": "本品类涵盖面向分布式站点及相关项目环境的通信电源设备与直流支持模块。",
        "Base stations and telecom rooms": "基站与通信机房",
        "Remote communication deployments": "偏远通信部署",
        "Industrial DC support scenarios": "工业直流支持场景",
        "Rectifier systems": "整流系统",
        "DC modules and support hardware": "直流模块及支持硬件",
        "Monitoring and protection accessories": "监控与保护配件",
        "Supports telecom-focused projects with practical category scope.": "以务实品类范围支持通信导向项目。",
        "Combines core DC equipment with supporting accessories.": "将核心直流设备与支持配件相结合。",
        "Adapts well to distributed deployment conditions.": "良好适配分布式部署条件。",
        "Monitoring & Industrial Cabling": "监控与工业线缆",
        "Monitoring accessories, sensing components, and industrial cabling for power integration and supervision applications.": "面向电源集成与监管应用的监控配件、传感组件及工业线缆。",
        "Monitoring accessories and industrial integration equipment": "监控配件与工业集成设备",
        "This category helps complete projects that need sensing accessories, monitoring items, and industrial cabling rather than only primary equipment.": "本品类帮助完善需要传感配件、监控件及工业线缆而不仅是主设备的工程。",
        "Environmental and safety monitoring": "环境与安全监控",
        "Power accessory completion": "电源配件补全",
        "Industrial integration projects": "工业集成项目",
        "Sensors and probes": "传感器与探头",
        "M12 and industrial connection cabling": "M12 及工业连接线缆",
        "Monitoring accessories and field parts": "监控配件与现场部件",
        "Completes the accessory layer of power projects.": "完善电源项目的配件层。",
        "Supports bundled sourcing for field deployment.": "支持现场部署的捆绑采购。",
        "Improves project readiness with integration parts included.": "通过纳入集成件提升项目就绪度。",
    }


def load_fr_map() -> dict[str, str]:
    from translation_data_fr import FR_MAP  # noqa: WPS433

    return FR_MAP


def load_ru_map() -> dict[str, str]:
    from translation_data_ru import RU_MAP  # noqa: WPS433

    return RU_MAP


def write_map(lang: str, mapping: dict[str, str], strings: list[str]) -> None:
    missing = [s for s in strings if s not in mapping]
    if missing:
        print(f"{lang} missing {len(missing)} strings")
        (OUT_DIR / f"_{lang}_missing.txt").write_text("\n".join(missing), encoding="utf-8")
        return
    (OUT_DIR / f"{lang}.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {lang}.json with {len(mapping)} entries")


def main() -> None:
    from translation_data_part2 import PART2_ZH  # noqa: WPS433

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    strings = STRINGS_FILE.read_text(encoding="utf-8").splitlines()
    zm = {**zh_map(), **PART2_ZH}
    write_map("zh", zm, strings)
    write_map("fr", load_fr_map(), strings)
    write_map("ru", load_ru_map(), strings)


if __name__ == "__main__":
    main()
