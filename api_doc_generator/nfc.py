from api_doc_common import *

nfc = Module("nfc", "NFC-Ladefreigabe", "Benötigt das Feature <a href=\"#features_nfc\"><code>\"nfc\"</code></a>.", Version.WARP1 | Version.WARP2, [
    Func("seen_tags", FuncType.STATE, Elem.ARRAY("Die zuletzt von der Wallbox gesehenen NFC-Tags.", members=[
            * 8 * [Elem.OBJECT("Ein gesehenes NFC-Tag", members = {
                "tag_type": Elem.INT("Typ des Tags", constants=[
                    Const(0, "Mifare Classic"),
                    Const(1, "NFC Forum Typ 1"),
                    Const(2, "NFC Forum Typ 2"),
                    Const(3, "NFC Forum Typ 3"),
                    Const(4, "NFC Forum Typ 4"),
                ]),
                "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
                "last_seen": Elem.INT("Zeit in Millisekunden vor der das Tag zuletzt gesehen wurde.", unit=Units.ms)
            })],
            Elem.OBJECT("Das von {{{ref:nfc/inject_tag}}} vorgetäuschte Tag", members = {
                "tag_type": Elem.INT("Typ des Tags", constants=[
                    Const(0, "Mifare Classic"),
                    Const(1, "NFC Forum Typ 1"),
                    Const(2, "NFC Forum Typ 2"),
                    Const(3, "NFC Forum Typ 3"),
                    Const(4, "NFC Forum Typ 4"),
                ]),
                "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
                "last_seen": Elem.INT("Zeit in Millisekunden vor der das Tag zuletzt gesehen wurde.", unit=Units.ms)
            })
        ])
    ),

    Func("inject_tag", FuncType.COMMAND, Elem.OBJECT("Täuscht vor, dass ein Tag vom NFC-Leser erkannt wurde. Hiermit kann über die API ein Ladevorgang für einen bestimmten Benutzer gestartet oder gestoppt werden. Analog zur physischen Verwendung eines Tags wird der Ladevorgang bei Aufruf der API abwechselnd freigegeben oder blockiert. Siehe {{{ref:nfc/inject_tag_start}}} und {{{ref:nfc/inject_tag_stop}}} für genauere Kontrolle. Das vorgetauschte Tag ist immer der letzte Eintrag in {{{ref:nfc/seen_tags}}}", members={
        "tag_type": Elem.INT("Typ des Tags.", constants=[
            Const(0, "Mifare Classic"),
            Const(1, "NFC Forum Typ 1"),
            Const(2, "NFC Forum Typ 2"),
            Const(3, "NFC Forum Typ 3"),
            Const(4, "NFC Forum Typ 4"),
        ]),
        "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
    }), True),

     Func("inject_tag_start", FuncType.COMMAND, Elem.OBJECT("Täuscht vor, dass ein Tag vom NFC-Leser erkannt wurde. Das Tag wird nur zum <strong>Starten</strong> eines Ladevorgangs verwendet. Das vorgetauschte Tag ist immer der letzte Eintrag in {{{ref:nfc/seen_tags}}}", members={
        "tag_type": Elem.INT("Typ des Tags.", constants=[
            Const(0, "Mifare Classic"),
            Const(1, "NFC Forum Typ 1"),
            Const(2, "NFC Forum Typ 2"),
            Const(3, "NFC Forum Typ 3"),
            Const(4, "NFC Forum Typ 4"),
        ]),
        "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
    }), True),

     Func("inject_tag_stop", FuncType.COMMAND, Elem.OBJECT("Täuscht vor, dass ein Tag vom NFC-Leser erkannt wurde. Das Tag wird nur zum <strong>Stoppen</strong> eines Ladevorgangs verwendet. Das vorgetauschte Tag ist immer der letzte Eintrag in {{{ref:nfc/seen_tags}}}", members={
        "tag_type": Elem.INT("Typ des Tags.", constants=[
            Const(0, "Mifare Classic"),
            Const(1, "NFC Forum Typ 1"),
            Const(2, "NFC Forum Typ 2"),
            Const(3, "NFC Forum Typ 3"),
            Const(4, "NFC Forum Typ 4"),
        ]),
        "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
    }), True),

    Func("config", FuncType.CONFIGURATION, Elem.OBJECT("Die NFC-Konfiguration. Diese kann über nfc/config_update mit dem selben Payload aktualisiert werden.", members={
            "authorized_tags": Elem.ARRAY("Eine Liste authorisierter Tags.", members=[
                * 16 * [
                    Elem.OBJECT("Ein autorisiertes NFC-Tag", members={
                        "user_id": Elem.INT("ID des Nutzers dem dieses Tag zugeordnet ist, oder 0 falls es keinem Nutzer zugeordnet ist."),
                        "tag_type": Elem.INT("Typ des Tags.", constants=[
                            Const(0, "Mifare Classic"),
                            Const(1, "NFC Forum Typ 1"),
                            Const(2, "NFC Forum Typ 2"),
                            Const(3, "NFC Forum Typ 3"),
                            Const(4, "NFC Forum Typ 4"),
                        ]),
                        "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
                    })
                ]
            ]),
        })
    ),
])
