import json
import os
import shutil
import uuid

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, "output")
DATA_DIR = os.path.join(ROOT_DIR, "data")
REF_BASE_THEME = os.path.join(
    ROOT_DIR, "ref_test", "ref_test.Report", "StaticResources", "SharedResources", "BaseThemes", "Fluent2-CY26SU11.json"
)

THEME_JSON = {
    "name": "RoyalAuroraCrossSector",
    "dataColors": [
        "#06B6D4", "#8B5CF6", "#10B981", "#F59E0B",
        "#EC4899", "#3B82F6", "#F97316", "#14B8A6", "#A855F7"
    ],
    "background": "#0B1120",
    "foreground": "#F8FAFC",
    "tableAccent": "#06B6D4",
    "good": "#10B981",
    "neutral": "#F59E0B",
    "bad": "#EF4444",
    "visualStyles": {
        "page": {
            "*": {
                "background": [{"color": {"solid": {"color": "#0B1120"}}, "transparency": 0}],
                "outspace": [{"color": {"solid": {"color": "#060913"}}}]
            }
        },
        "*": {
            "*": {
                "background": [{"color": {"solid": {"color": "#131C31"}}, "transparency": 0}],
                "border": [{"show": True, "color": {"solid": {"color": "#253352"}}, "radius": 14}],
                "dropShadow": [{"show": True, "color": {"solid": {"color": "#020617"}}, "position": "Outer", "preset": "BottomRight"}],
                "title": [{"show": True, "fontColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 17, "fontFamily": "Segoe UI"}],
                "visualHeader": [{"show": False}]
            }
        },
        "card": {
            "*": {
                "background": [{"color": {"solid": {"color": "#17203A"}}, "transparency": 0}],
                "border": [{"show": True, "color": {"solid": {"color": "#3B82F6"}}, "radius": 14}],
                "labels": [{"color": {"solid": {"color": "#38BDF8"}}, "fontSize": 38, "fontFamily": "Segoe UI Semibold"}],
                "categoryLabels": [{"show": False}]
            }
        },
        "slicer": {
            "*": {
                "background": [{"color": {"solid": {"color": "#131C31"}}, "transparency": 0}],
                "border": [{"show": True, "color": {"solid": {"color": "#6366F1"}}, "radius": 14}],
                "items": [{"fontColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 16, "fontFamily": "Segoe UI"}]
            }
        },
        "tableEx": {
            "*": {
                "columnHeaders": [{"fontColor": {"solid": {"color": "#38BDF8"}}, "backColor": {"solid": {"color": "#0F172A"}}, "fontSize": 15, "fontFamily": "Segoe UI"}],
                "values": [{"fontColorPrimary": {"solid": {"color": "#F8FAFC"}}, "backColorPrimary": {"solid": {"color": "#131C31"}}, "fontColorSecondary": {"solid": {"color": "#E2E8F0"}}, "backColorSecondary": {"solid": {"color": "#19233C"}}, "fontSize": 15, "fontFamily": "Segoe UI"}],
                "total": [{"fontColor": {"solid": {"color": "#38BDF8"}}, "backColor": {"solid": {"color": "#0F172A"}}, "fontSize": 15, "fontFamily": "Segoe UI"}]
            }
        },
        "lineChart": {
            "*": {
                "lineStyles": [{"strokeWidth": 3, "lineStyle": "solid"}],
                "categoryAxis": [{"labelColor": {"solid": {"color": "#E2E8F0"}}, "fontSize": 14}],
                "valueAxis": [{"labelColor": {"solid": {"color": "#E2E8F0"}}, "fontSize": 14}],
                "legend": [{"show": True, "position": "Bottom", "fontColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}]
            }
        },
        "clusteredBarChart": {
            "*": {
                "categoryAxis": [{"labelColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}],
                "valueAxis": [{"labelColor": {"solid": {"color": "#E2E8F0"}}, "fontSize": 14}],
                "labels": [{"show": True, "color": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}],
                "legend": [{"show": True, "position": "Bottom", "fontColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}]
            }
        },
        "clusteredColumnChart": {
            "*": {
                "categoryAxis": [{"labelColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}],
                "valueAxis": [{"labelColor": {"solid": {"color": "#E2E8F0"}}, "fontSize": 14}],
                "labels": [{"show": True, "color": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}],
                "legend": [{"show": True, "position": "Bottom", "fontColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}]
            }
        },
        "scatterChart": {
            "*": {
                "categoryAxis": [{"labelColor": {"solid": {"color": "#E2E8F0"}}, "fontSize": 14}],
                "valueAxis": [{"labelColor": {"solid": {"color": "#E2E8F0"}}, "fontSize": 14}],
                "categoryLabels": [{"show": True, "color": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}],
                "legend": [{"show": True, "position": "Bottom", "fontColor": {"solid": {"color": "#F8FAFC"}}, "fontSize": 13}]
            }
        },
        "donutChart": {
            "*": {
                "labels": [{"show": True, "color": {"solid": {"color": "#F8FAFC"}}, "fontSize": 14}],
                "legend": [{"show": False}]
            }
        },
        "treemap": {
            "*": {
                "labels": [{"show": True, "color": {"solid": {"color": "#FFFFFF"}}, "fontSize": 16}],
                "legend": [{"show": False}]
            }
        }
    }
}

# Combines both aerospace_data.csv and mechanical_data.csv (2,775 total rows across 18 peers)
TMDL_TEMPLATE = """table CompanyData
\tlineageTag: __LINEAGE_TAG__

\tmeasure 'Total Market Cap' = CALCULATE(AVERAGE(CompanyData[Market_Cap_B]), CompanyData[Record_Type] = "Actual")
\t\tformatString: "#,0.0"

\tmeasure 'Projected AI Growth' = AVERAGEX(VALUES(CompanyData[Company]), DIVIDE(CALCULATE(LASTNONBLANKVALUE(CompanyData[Date], AVERAGE(CompanyData[Normalized_Index])), CompanyData[Record_Type] = "AI Forecast (3Y)") - CALCULATE(LASTNONBLANKVALUE(CompanyData[Date], AVERAGE(CompanyData[Normalized_Index])), CompanyData[Record_Type] = "Actual"), CALCULATE(LASTNONBLANKVALUE(CompanyData[Date], AVERAGE(CompanyData[Normalized_Index])), CompanyData[Record_Type] = "Actual"), 0))
\t\tformatString: "+0.0%;-0.0%;0.0%"

\tmeasure 'Historical Return' = AVERAGEX(VALUES(CompanyData[Company]), DIVIDE(CALCULATE(LASTNONBLANKVALUE(CompanyData[Date], AVERAGE(CompanyData[Normalized_Index])), CompanyData[Record_Type] = "Actual") - CALCULATE(FIRSTNONBLANKVALUE(CompanyData[Date], AVERAGE(CompanyData[Normalized_Index])), CompanyData[Record_Type] = "Actual"), CALCULATE(FIRSTNONBLANKVALUE(CompanyData[Date], AVERAGE(CompanyData[Normalized_Index])), CompanyData[Record_Type] = "Actual"), 0))
\t\tformatString: "+0.0%;-0.0%;0.0%"

\tmeasure 'Operating Margin' = AVERAGE(CompanyData[Operating_Margin_Pct]) / 100
\t\tformatString: "0.0%"

\tmeasure 'NLP Sentiment' = AVERAGE(CompanyData[NLP_Sentiment_Score])
\t\tformatString: "0.0"

\tmeasure 'Performance Index' = AVERAGE(CompanyData[Normalized_Index])
\t\tformatString: "#,0.0"

\tmeasure 'Forecast Upper' = AVERAGE(CompanyData[Forecast_Upper_Index])
\t\tformatString: "#,0.0"

\tmeasure 'Forecast Lower' = AVERAGE(CompanyData[Forecast_Lower_Index])
\t\tformatString: "#,0.0"

\tmeasure 'Annual Revenue RunRate' = AVERAGE(CompanyData[Monthly_Revenue_B]) * 12
\t\tformatString: "#,0.0"

\tmeasure 'Return on Equity' = AVERAGE(CompanyData[ROE_Pct]) / 100
\t\tformatString: "0.0%"

\tmeasure 'Debt to Equity' = AVERAGE(CompanyData[Debt_to_Equity])
\t\tformatString: "0.00"

\tcolumn Industry
\t\tdataType: string
\t\tsourceColumn: Industry

\tcolumn Ticker
\t\tdataType: string
\t\tsourceColumn: Ticker

\tcolumn Company
\t\tdataType: string
\t\tsourceColumn: Company

\tcolumn Date
\t\tdataType: dateTime
\t\tformatString: yyyy-mm-dd
\t\tsourceColumn: Date

\tcolumn Record_Type
\t\tdataType: string
\t\tsourceColumn: Record_Type

\tcolumn Close_Price
\t\tdataType: double
\t\tsourceColumn: Close_Price

\tcolumn Normalized_Index
\t\tdataType: double
\t\tsourceColumn: Normalized_Index

\tcolumn Monthly_Revenue_B
\t\tdataType: double
\t\tsourceColumn: Monthly_Revenue_B

\tcolumn Operating_Margin_Pct
\t\tdataType: double
\t\tsourceColumn: Operating_Margin_Pct

\tcolumn ROE_Pct
\t\tdataType: double
\t\tsourceColumn: ROE_Pct

\tcolumn Debt_to_Equity
\t\tdataType: double
\t\tsourceColumn: Debt_to_Equity

\tcolumn Market_Cap_B
\t\tdataType: double
\t\tsourceColumn: Market_Cap_B

\tcolumn NLP_Sentiment_Score
\t\tdataType: double
\t\tsourceColumn: NLP_Sentiment_Score

\tcolumn Forecast_Lower_Index
\t\tdataType: double
\t\tsourceColumn: Forecast_Lower_Index

\tcolumn Forecast_Upper_Index
\t\tdataType: double
\t\tsourceColumn: Forecast_Upper_Index

\tpartition CompanyData = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    AeroRaw = Csv.Document(File.Contents("__AERO_CSV__"),[Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    AeroPromoted = Table.PromoteHeaders(AeroRaw, [PromoteAllScalars=true]),
\t\t\t    MechRaw = Csv.Document(File.Contents("__MECH_CSV__"),[Delimiter=",", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    MechPromoted = Table.PromoteHeaders(MechRaw, [PromoteAllScalars=true]),
\t\t\t    Combined = Table.Combine({AeroPromoted, MechPromoted}),
\t\t\t    Typed = Table.TransformColumnTypes(Combined,{{"Date", type date}, {"Close_Price", type number}, {"Normalized_Index", type number}, {"Monthly_Revenue_B", type number}, {"Operating_Margin_Pct", type number}, {"ROE_Pct", type number}, {"Debt_to_Equity", type number}, {"Market_Cap_B", type number}, {"NLP_Sentiment_Score", type number}, {"Forecast_Lower_Index", type number}, {"Forecast_Upper_Index", type number}})
\t\t\tin
\t\t\t    Typed
"""

def hex20() -> str:
    return uuid.uuid4().hex[:20]

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

def write_json(path: str, data: dict):
    write_file(path, json.dumps(data, indent=2))

def measure_field(entity: str, prop: str):
    return {
        "field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop
    }

def column_field(entity: str, prop: str):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop
    }

def build_industry_page_filter(industry_name: str):
    return [{
        "name": hex20(),
        "field": {
            "Column": {
                "Expression": {"SourceRef": {"Entity": "CompanyData"}},
                "Property": "Industry"
            }
        },
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": "c", "Entity": "CompanyData", "Type": 0}],
            "Where": [{
                "Condition": {
                    "In": {
                        "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": "Industry"}}],
                        "Values": [[{"Literal": {"Value": f"'{industry_name}'"}}]]
                    }
                }
            }]
        }
    }]

def build_visual_json(visual_id: str, x: int, y: int, w: int, h: int, z: int, visual_type: str, title: str, query_projections: dict):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.15.0/schema.json",
        "name": visual_id,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": visual_type,
            "query": {"queryState": query_projections},
            "visualContainerObjects": {
                "title": [{
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "text": {"expr": {"Literal": {"Value": f"'{title}'"}}}
                    }
                }]
            },
            "drillFilterOtherVisuals": True
        }
    }

def build_banner_textbox(visual_id: str, x: int, y: int, w: int, h: int, z: int, heading: str, subheading: str):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.15.0/schema.json",
        "name": visual_id,
        "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [
                                {"value": heading + "\n", "textStyle": {"fontWeight": "bold", "fontSize": "22pt", "color": "#38BDF8"}},
                                {"value": subheading, "textStyle": {"fontSize": "13pt", "color": "#E2E8F0"}}
                            ]
                        }]
                    }
                }]
            },
            "visualContainerObjects": {
                "background": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#17203A'"}}}}}}}],
                "border": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}, "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#8B5CF6'"}}}}}, "radius": {"expr": {"Literal": {"Value": "14D"}}}}}]
            }
        }
    }

def write_page(rep_dir: str, page_id: str, display_name: str, visuals: list, page_filters: list = None):
    page_payload = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": page_id,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": 900,
        "width": 1600
    }
    if page_filters:
        page_payload["filterConfig"] = {"filters": page_filters}

    write_json(os.path.join(rep_dir, "definition", "pages", page_id, "page.json"), page_payload)
    for v in visuals:
        v_id = v["name"]
        write_json(os.path.join(rep_dir, "definition", "pages", page_id, "visuals", v_id, "visual.json"), v)

def generate_dashboard(primary_industry: str, aero_csv: str, mech_csv: str):
    proj_name = f"{primary_industry}_Intelligence"
    root = os.path.join(BASE_DIR, proj_name)
    sm_dir = os.path.join(root, f"{proj_name}.SemanticModel")
    rep_dir = os.path.join(root, f"{proj_name}.Report")

    if os.path.exists(root):
        shutil.rmtree(root, ignore_errors=True)

    write_json(os.path.join(root, f"{proj_name}.pbip"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{proj_name}.Report"}}],
        "settings": {"enableAutoRecovery": True}
    })

    write_json(os.path.join(sm_dir, ".platform"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": proj_name},
        "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}
    })
    write_json(os.path.join(sm_dir, "definition.pbism"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/1.0.0/schema.json",
        "version": "4.0",
        "settings": {}
    })
    write_file(os.path.join(sm_dir, "definition", "database.tmdl"), "database Database\n\tcompatibilityLevel: 1567\n")
    write_file(os.path.join(sm_dir, "definition", "model.tmdl"), "model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\nref table CompanyData\n")

    tmdl_table = (
        TMDL_TEMPLATE
        .replace("__LINEAGE_TAG__", str(uuid.uuid4()))
        .replace("__AERO_CSV__", aero_csv.replace("\\", "\\\\"))
        .replace("__MECH_CSV__", mech_csv.replace("\\", "\\\\"))
    )
    write_file(os.path.join(sm_dir, "definition", "tables", "CompanyData.tmdl"), tmdl_table)

    write_json(os.path.join(rep_dir, ".platform"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": proj_name},
        "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}
    })
    write_json(os.path.join(rep_dir, "definition.pbir"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/1.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{proj_name}.SemanticModel"}}
    })
    write_json(os.path.join(rep_dir, "definition", "version.json"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "2.0.0"
    })

    base_theme_dst = os.path.join(rep_dir, "StaticResources", "SharedResources", "BaseThemes", "Fluent2-CY26SU11.json")
    os.makedirs(os.path.dirname(base_theme_dst), exist_ok=True)
    if os.path.exists(REF_BASE_THEME):
        shutil.copy2(REF_BASE_THEME, base_theme_dst)

    custom_theme_dst = os.path.join(rep_dir, "StaticResources", "RegisteredResources", "RoyalAuroraCrossSector.json")
    write_json(custom_theme_dst, THEME_JSON)

    resource_packages = [{
        "name": "RegisteredResources",
        "type": "RegisteredResources",
        "items": [{"name": "RoyalAuroraCrossSector.json", "path": "RoyalAuroraCrossSector.json", "type": "CustomTheme"}]
    }]
    if os.path.exists(base_theme_dst):
        resource_packages.insert(0, {
            "name": "SharedResources",
            "type": "SharedResources",
            "items": [{"name": "Fluent2-CY26SU11", "path": "BaseThemes/Fluent2-CY26SU11.json", "type": "BaseTheme"}]
        })

    write_json(os.path.join(rep_dir, "definition", "report.json"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.4.0/schema.json",
        "themeCollection": {
            "baseTheme": {
                "name": "Fluent2-CY26SU11",
                "reportVersionAtImport": {"visual": "2.15.0", "report": "3.4.0", "page": "2.3.1"},
                "type": "SharedResources"
            },
            "customTheme": {
                "name": "RoyalAuroraCrossSector.json",
                "reportVersionAtImport": {"visual": "2.15.0", "report": "3.4.0", "page": "2.3.1"},
                "type": "RegisteredResources"
            }
        },
        "objects": {
            "section": [{"properties": {"verticalAlignment": {"expr": {"Literal": {"Value": "'Top'"}}}}}]
        },
        "resourcePackages": resource_packages,
        "settings": {
            "useStylableVisualContainerHeader": True,
            "exportDataMode": "AllowSummarized",
            "defaultDrillFilterOtherVisuals": True,
            "allowChangeFilterTypes": True,
            "useEnhancedTooltips": True,
            "useDefaultAggregateDisplayName": True
        }
    })

    page1_id = hex20()
    page2_id = hex20()
    page3_id = hex20()
    page4_id = hex20()
    write_json(os.path.join(rep_dir, "definition", "pages", "pages.json"), {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [page1_id, page2_id, page3_id, page4_id],
        "activePageName": page1_id
    })

    sector_lock = build_industry_page_filter(primary_industry)

    # === PAGE 1: EXECUTIVE COMMAND CENTER (Locked to primary_industry) ===
    page1_visuals = [
        build_banner_textbox(hex20(), 16, 16, 284, 176, 900, f"{primary_industry.upper()} SUITE", "10Y Market & 3Y AI Forecast"),
        build_visual_json(hex20(), 16, 204, 284, 468, 1000, "slicer", f"FILTER {primary_industry.upper()} PEERS", {
            "Values": {"projections": [column_field("CompanyData", "Company")]}
        }),
        build_visual_json(hex20(), 16, 684, 284, 200, 1100, "slicer", "TIMELINE HORIZON", {
            "Values": {"projections": [column_field("CompanyData", "Record_Type")]}
        }),
        build_visual_json(hex20(), 312, 16, 308, 176, 2000, "card", "AVG MARKET CAP (B)", {
            "Values": {"projections": [measure_field("CompanyData", "Total Market Cap")]}
        }),
        build_visual_json(hex20(), 632, 16, 308, 176, 2100, "card", "3Y AI GROWTH", {
            "Values": {"projections": [measure_field("CompanyData", "Projected AI Growth")]}
        }),
        build_visual_json(hex20(), 952, 16, 308, 176, 2200, "card", "OPERATING MARGIN", {
            "Values": {"projections": [measure_field("CompanyData", "Operating Margin")]}
        }),
        build_visual_json(hex20(), 1272, 16, 312, 176, 2300, "card", "NLP SENTIMENT", {
            "Values": {"projections": [measure_field("CompanyData", "NLP Sentiment")]}
        }),
        build_visual_json(hex20(), 312, 204, 800, 340, 3000, "lineChart", "10Y HISTORICAL & 3Y AI GROWTH TRAJECTORY (BASE 100)", {
            "Category": {"projections": [column_field("CompanyData", "Date")]},
            "Series": {"projections": [column_field("CompanyData", "Company")]},
            "Y": {"projections": [measure_field("CompanyData", "Performance Index")]}
        }),
        build_visual_json(hex20(), 1124, 204, 460, 340, 3100, "scatterChart", "MARGIN VS. 3Y AI GROWTH", {
            "Category": {"projections": [column_field("CompanyData", "Company")]},
            "Series": {"projections": [column_field("CompanyData", "Company")]},
            "X": {"projections": [measure_field("CompanyData", "Operating Margin")]},
            "Y": {"projections": [measure_field("CompanyData", "Projected AI Growth")]},
            "Size": {"projections": [measure_field("CompanyData", "Total Market Cap")]}
        }),
        build_visual_json(hex20(), 312, 556, 420, 328, 4000, "clusteredBarChart", "3Y AI GROWTH LEADERBOARD", {
            "Category": {"projections": [column_field("CompanyData", "Company")]},
            "Y": {"projections": [measure_field("CompanyData", "Projected AI Growth")]}
        }),
        build_visual_json(hex20(), 744, 556, 340, 328, 4100, "donutChart", "REVENUE SHARE (B)", {
            "Category": {"projections": [column_field("CompanyData", "Company")]},
            "Y": {"projections": [measure_field("CompanyData", "Annual Revenue RunRate")]}
        }),
        build_visual_json(hex20(), 1096, 556, 488, 328, 4200, "tableEx", "PEER FUNDAMENTALS & AI SIGNALS", {
            "Values": {"projections": [
                column_field("CompanyData", "Company"),
                measure_field("CompanyData", "Projected AI Growth"),
                measure_field("CompanyData", "Operating Margin"),
                measure_field("CompanyData", "NLP Sentiment")
            ]}
        })
    ]
    write_page(rep_dir, page1_id, f"{primary_industry} Command Center", page1_visuals, page_filters=sector_lock)

    # === PAGE 2: COMPANY DEEP-DIVE & 3Y AI CONFIDENCE CONE (Locked to primary_industry) ===
    page2_visuals = [
        build_banner_textbox(hex20(), 16, 16, 284, 176, 900, "AI FORECAST", "Select 1 Company for 3Y Cone"),
        build_visual_json(hex20(), 16, 204, 284, 680, 1000, "slicer", f"SELECT {primary_industry.upper()} COMPANY", {
            "Values": {"projections": [column_field("CompanyData", "Company")]}
        }),
        build_visual_json(hex20(), 312, 16, 308, 176, 2000, "card", "10Y RETURN", {
            "Values": {"projections": [measure_field("CompanyData", "Historical Return")]}
        }),
        build_visual_json(hex20(), 632, 16, 308, 176, 2100, "card", "3Y AI GROWTH", {
            "Values": {"projections": [measure_field("CompanyData", "Projected AI Growth")]}
        }),
        build_visual_json(hex20(), 952, 16, 308, 176, 2200, "card", "ANNUAL REVENUE (B)", {
            "Values": {"projections": [measure_field("CompanyData", "Annual Revenue RunRate")]}
        }),
        build_visual_json(hex20(), 1272, 16, 312, 176, 2300, "card", "RETURN ON EQUITY", {
            "Values": {"projections": [measure_field("CompanyData", "Return on Equity")]}
        }),
        build_visual_json(hex20(), 312, 204, 1272, 356, 3000, "lineChart", "10Y ACTUALS + 3Y AI CONFIDENCE CONE (MEDIAN, UPPER 85% & LOWER 15% BOUNDS)", {
            "Category": {"projections": [column_field("CompanyData", "Date")]},
            "Y": {"projections": [
                measure_field("CompanyData", "Performance Index"),
                measure_field("CompanyData", "Forecast Upper"),
                measure_field("CompanyData", "Forecast Lower")
            ]}
        }),
        build_visual_json(hex20(), 312, 572, 1272, 312, 4000, "areaChart", "HISTORICAL & AI-PROJECTED ANNUALIZED REVENUE RUN-RATE (B)", {
            "Category": {"projections": [column_field("CompanyData", "Date")]},
            "Y": {"projections": [measure_field("CompanyData", "Annual Revenue RunRate")]}
        })
    ]
    write_page(rep_dir, page2_id, "Company AI Forecast Cone", page2_visuals, page_filters=sector_lock)

    # === PAGE 3: PEER VALUATION & FINANCIAL HEALTH MATRIX (Locked to primary_industry) ===
    page3_visuals = [
        build_banner_textbox(hex20(), 16, 16, 1568, 92, 900, f"{primary_industry.upper()} PEER BENCHMARKING & FINANCIAL HEALTH MATRIX", "10-Year Historical Return vs. 3-Year AI Forward Growth, Capital Efficiency (ROE) & Leverage"),
        build_visual_json(hex20(), 16, 120, 778, 372, 2000, "clusteredColumnChart", "10Y HISTORICAL RETURN VS. 3Y AI GROWTH", {
            "Category": {"projections": [column_field("CompanyData", "Company")]},
            "Y": {"projections": [
                measure_field("CompanyData", "Historical Return"),
                measure_field("CompanyData", "Projected AI Growth")
            ]}
        }),
        build_visual_json(hex20(), 806, 120, 778, 372, 2100, "clusteredBarChart", "RETURN ON EQUITY (ROE %) & OPERATING MARGIN", {
            "Category": {"projections": [column_field("CompanyData", "Company")]},
            "Y": {"projections": [
                measure_field("CompanyData", "Return on Equity"),
                measure_field("CompanyData", "Operating Margin")
            ]}
        }),
        build_visual_json(hex20(), 16, 504, 460, 380, 3000, "treemap", "MARKET CAP SHARE (B)", {
            "Group": {"projections": [column_field("CompanyData", "Company")]},
            "Values": {"projections": [measure_field("CompanyData", "Total Market Cap")]}
        }),
        build_visual_json(hex20(), 488, 504, 1096, 380, 3100, "tableEx", "COMPLETE EXECUTIVE FINANCIAL & AI SCORECARD", {
            "Values": {"projections": [
                column_field("CompanyData", "Ticker"),
                column_field("CompanyData", "Company"),
                measure_field("CompanyData", "Total Market Cap"),
                measure_field("CompanyData", "Annual Revenue RunRate"),
                measure_field("CompanyData", "Historical Return"),
                measure_field("CompanyData", "Projected AI Growth"),
                measure_field("CompanyData", "Operating Margin"),
                measure_field("CompanyData", "Return on Equity"),
                measure_field("CompanyData", "Debt to Equity"),
                measure_field("CompanyData", "NLP Sentiment")
            ]}
        })
    ]
    write_page(rep_dir, page3_id, "Peer Financial Matrix", page3_visuals, page_filters=sector_lock)

    # === PAGE 4: COMBINED CROSS-SECTOR COMPARISON (Aerospace vs. Mechanical - All 18 Companies) ===
    page4_visuals = [
        build_banner_textbox(hex20(), 16, 16, 284, 176, 900, "CROSS-SECTOR", "Aerospace vs. Mechanical (18 Peers)"),
        build_visual_json(hex20(), 16, 204, 284, 196, 1000, "slicer", "FILTER SECTOR", {
            "Values": {"projections": [column_field("CompanyData", "Industry")]}
        }),
        build_visual_json(hex20(), 16, 412, 284, 472, 1100, "slicer", "FILTER ALL 18 COMPANIES", {
            "Values": {"projections": [column_field("CompanyData", "Company")]}
        }),
        build_visual_json(hex20(), 312, 16, 308, 176, 2000, "card", "COMBINED 10Y RETURN", {
            "Values": {"projections": [measure_field("CompanyData", "Historical Return")]}
        }),
        build_visual_json(hex20(), 632, 16, 308, 176, 2100, "card", "COMBINED 3Y AI GROWTH", {
            "Values": {"projections": [measure_field("CompanyData", "Projected AI Growth")]}
        }),
        build_visual_json(hex20(), 952, 16, 308, 176, 2200, "card", "AVG OPERATING MARGIN", {
            "Values": {"projections": [measure_field("CompanyData", "Operating Margin")]}
        }),
        build_visual_json(hex20(), 1272, 16, 312, 176, 2300, "card", "AVG RETURN ON EQUITY", {
            "Values": {"projections": [measure_field("CompanyData", "Return on Equity")]}
        }),
        build_visual_json(hex20(), 312, 204, 632, 340, 3000, "lineChart", "AEROSPACE VS. MECHANICAL 10Y & 3Y TRAJECTORY (BASE 100)", {
            "Category": {"projections": [column_field("CompanyData", "Date")]},
            "Series": {"projections": [column_field("CompanyData", "Industry")]},
            "Y": {"projections": [measure_field("CompanyData", "Performance Index")]}
        }),
        build_visual_json(hex20(), 956, 204, 628, 340, 3100, "clusteredColumnChart", "SECTOR HEAD-TO-HEAD: AI GROWTH, MARGIN & ROE", {
            "Category": {"projections": [column_field("CompanyData", "Industry")]},
            "Y": {"projections": [
                measure_field("CompanyData", "Projected AI Growth"),
                measure_field("CompanyData", "Operating Margin"),
                measure_field("CompanyData", "Return on Equity")
            ]}
        }),
        build_visual_json(hex20(), 312, 556, 540, 328, 4000, "scatterChart", "ALL 18 PEERS: MARGIN VS. 3Y AI GROWTH", {
            "Category": {"projections": [column_field("CompanyData", "Company")]},
            "Series": {"projections": [column_field("CompanyData", "Industry")]},
            "X": {"projections": [measure_field("CompanyData", "Operating Margin")]},
            "Y": {"projections": [measure_field("CompanyData", "Projected AI Growth")]},
            "Size": {"projections": [measure_field("CompanyData", "Total Market Cap")]}
        }),
        build_visual_json(hex20(), 864, 556, 720, 328, 4100, "tableEx", "CROSS-SECTOR EXECUTIVE LEADERBOARD (18 COMPANIES)", {
            "Values": {"projections": [
                column_field("CompanyData", "Industry"),
                column_field("CompanyData", "Company"),
                measure_field("CompanyData", "Historical Return"),
                measure_field("CompanyData", "Projected AI Growth"),
                measure_field("CompanyData", "Operating Margin"),
                measure_field("CompanyData", "Return on Equity")
            ]}
        })
    ]
    write_page(rep_dir, page4_id, "Cross-Sector Comparison", page4_visuals, page_filters=None)

    print(f"Generated 4-page Cross-Sector PBIP dashboard -> {os.path.join(root, proj_name + '.pbip')}")

if __name__ == "__main__":
    aero_path = os.path.join(DATA_DIR, "aerospace_data.csv")
    mech_path = os.path.join(DATA_DIR, "mechanical_data.csv")
    generate_dashboard("Aerospace", aero_path, mech_path)
    generate_dashboard("Mechanical", aero_path, mech_path)