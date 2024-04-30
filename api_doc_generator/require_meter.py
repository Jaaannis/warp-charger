from api_doc_common import *

require_meter = Module("require_meter", "Zählerüberwachung", "", "", Version.CHARGER, [
    Func("config", FuncType.CONFIGURATION, Elem.OBJECT("Die Konfiguration der Zählerüberwachung.", members={
        "config": Elem.INT("Konfiguration der Zählerüberwachung.", constants=[
            Const(0, "Es wurde noch nie ein Stromzähler gesehen. Zählerüberwachung deaktiviert. Sobald das erste Mal ein Stromzähler erkannt wird, wird dieser Wert automatisch auf 1 geändert."),
            Const(1, "Es wurde bereits einmal ein Stromzähler gesehen. Zählerüberwachung aktiviert."),
            Const(2, "Es wurde bereits einmal ein Stromzähler gesehen. Zählerüberwachung deaktiviert."),
        ])
    }))
])
