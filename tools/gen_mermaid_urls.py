import base64


def b64url(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii").rstrip("=")


MERMAID_DARK = """%%{init: {'theme': 'dark', 'themeVariables': { 'primaryColor': '#1f2937', 'mainBkg': '#1f2937', 'clusterBkg': '#111827', 'clusterBorder': '#374151', 'lineColor': '#9ca3af', 'fontFamily': 'Segoe UI, sans-serif', 'edgeLabelBackground': '#111827' }}}%%
graph LR
    subgraph Inputs ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Inputs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        EEP["EEP file (.eep)" ]:::data
        VAR["Variant (OptionMenu)" ]:::data
        VER["Version fields\nmajor/minor/revision (0-99)" ]:::data
    end

    subgraph UI ["&nbsp;&nbsp;&nbsp;&nbsp;CustomTkinter UI&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        APP["VariantGeneratorDemoApp" ]:::ui
        OPEN["Open EEP file\n(file dialog)" ]:::ui
        GEN["Generate Results" ]:::ui
        SHOW["Status / errors\n(display_box)" ]:::ui
        EXP["Open created file\n(Explorer select)" ]:::ui
    end

    subgraph Logic ["&nbsp;&nbsp;&nbsp;&nbsp;Processing Pipeline&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        VAL["Validate inputs\n(EEP + 0..99)" ]:::proc
        MAP["Map product name -> ID\n(product_demo_data.py)" ]:::proc
        CMD["Build command\ncmd /c demo_writeheader.bat ..." ]:::proc
        RUN["Run subprocess\n(subprocess.run)" ]:::proc
        LOG["Append ChangeLog.txt\n(add_line_to_file)" ]:::proc
        OUTCHK{"demo.mot exists?"}:::proc
    end

    subgraph Outputs ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Outputs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        BAT["demo_writeheader.bat" ]:::data
        MOT["demo.mot" ]:::data
        CHG["ChangeLog.txt" ]:::data
        ERR["Error message" ]:::data
    end

    OPEN --> EEP
    APP --> OPEN
    APP --> GEN

    EEP --> VAL
    VAR --> MAP
    VER --> VAL

    VAL --> CMD
    MAP --> CMD
    CMD --> BAT
    BAT --> RUN
    RUN --> OUTCHK

    OUTCHK -- yes --> MOT
    OUTCHK -- yes --> LOG
    LOG --> CHG

    OUTCHK -- no --> ERR
    ERR --> SHOW

    MOT --> EXP

    classDef data fill:#172554,stroke:#60a5fa,stroke-width:2px,color:#dbeafe,rx:8,ry:8;
    classDef proc fill:#2e1065,stroke:#a78bfa,stroke-width:2px,color:#f3e8ff,rx:8,ry:8;
    classDef ui fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#d1fae5,rx:8,ry:8;
    style Inputs fill:#111827,stroke:#374151,stroke-width:1px,rx:10,ry:10
    style Logic fill:#111827,stroke:#374151,stroke-width:1px,rx:10,ry:10
    style UI fill:#111827,stroke:#374151,stroke-width:1px,rx:10,ry:10
    style Outputs fill:#111827,stroke:#374151,stroke-width:1px,rx:10,ry:10
"""


MERMAID_LIGHT = """%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#fff', 'mainBkg': '#fff', 'clusterBkg': '#f9fafb', 'clusterBorder': '#e5e7eb', 'lineColor': '#6b7280', 'fontFamily': 'Segoe UI, sans-serif', 'edgeLabelBackground': '#f9fafb' }}}%%
graph LR
    subgraph Inputs ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Inputs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        EEP["EEP file (.eep)" ]:::data
        VAR["Variant (OptionMenu)" ]:::data
        VER["Version fields\nmajor/minor/revision (0-99)" ]:::data
    end

    subgraph UI ["&nbsp;&nbsp;&nbsp;&nbsp;CustomTkinter UI&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        APP["VariantGeneratorDemoApp" ]:::ui
        OPEN["Open EEP file\n(file dialog)" ]:::ui
        GEN["Generate Results" ]:::ui
        SHOW["Status / errors\n(display_box)" ]:::ui
        EXP["Open created file\n(Explorer select)" ]:::ui
    end

    subgraph Logic ["&nbsp;&nbsp;&nbsp;&nbsp;Processing Pipeline&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        VAL["Validate inputs\n(EEP + 0..99)" ]:::proc
        MAP["Map product name -> ID\n(product_demo_data.py)" ]:::proc
        CMD["Build command\ncmd /c demo_writeheader.bat ..." ]:::proc
        RUN["Run subprocess\n(subprocess.run)" ]:::proc
        LOG["Append ChangeLog.txt\n(add_line_to_file)" ]:::proc
        OUTCHK{"demo.mot exists?"}:::proc
    end

    subgraph Outputs ["&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Outputs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"]
        direction TB
        BAT["demo_writeheader.bat" ]:::data
        MOT["demo.mot" ]:::data
        CHG["ChangeLog.txt" ]:::data
        ERR["Error message" ]:::data
    end

    OPEN --> EEP
    APP --> OPEN
    APP --> GEN

    EEP --> VAL
    VAR --> MAP
    VER --> VAL

    VAL --> CMD
    MAP --> CMD
    CMD --> BAT
    BAT --> RUN
    RUN --> OUTCHK

    OUTCHK -- yes --> MOT
    OUTCHK -- yes --> LOG
    LOG --> CHG

    OUTCHK -- no --> ERR
    ERR --> SHOW

    MOT --> EXP

    classDef data fill:#eff6ff,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a,rx:8,ry:8;
    classDef proc fill:#f5f3ff,stroke:#8b5cf6,stroke-width:2px,color:#4c1d95,rx:8,ry:8;
    classDef ui fill:#ecfdf5,stroke:#10b981,stroke-width:2px,color:#064e3b,rx:8,ry:8;
    style Inputs fill:#f9fafb,stroke:#e5e7eb,stroke-width:1px,rx:10,ry:10
    style Logic fill:#f9fafb,stroke:#e5e7eb,stroke-width:1px,rx:10,ry:10
    style UI fill:#f9fafb,stroke:#e5e7eb,stroke-width:1px,rx:10,ry:10
    style Outputs fill:#f9fafb,stroke:#e5e7eb,stroke-width:1px,rx:10,ry:10
"""


def main() -> None:
    dark_payload = b64url(MERMAID_DARK)
    light_payload = b64url(MERMAID_LIGHT)

    dark_url = "https://mermaid.ink/svg/" + dark_payload
    light_url = "https://mermaid.ink/svg/" + light_payload

    # Printing can wrap in some terminals; write to a file for easy copy/paste.
    out_path = "tools/mermaid_urls.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("DARK_URL=" + dark_url + "\n")
        f.write("LIGHT_URL=" + light_url + "\n")

    print("Wrote " + out_path)


if __name__ == "__main__":
    main()
