from api_doc_common import *

automation = Module("automation", "Automatisierung", "", "", Version.ANY, [
    Func("state", FuncType.STATE, Elem.OBJECT("Der Zustand der Automatisierung.", members={
        "registered_triggers": Elem.ARRAY("Dieser Firmware bekannte Bedingungen (Union-Tags des Triggers einer Regel aus {{{ref:automation/config}}})", members=[
            * 18 * [Elem.INT("Eine bekannte Bedingung.")]]),
        "registered_actions": Elem.ARRAY("Dieser Firmware bekannte Aktionen (Union-Tags der Aktion einer Regel aus {{{ref:automation/config}}})", members=[
            * 15 * [Elem.INT("Eine bekannte Bedingung.")]]),

        "enabled_triggers": Elem.ARRAY("Aktuell ausführbare Bedingungen (Union-Tags des Triggers einer Regel aus {{{ref:automation/config}}})", members=[
            * 18 * [Elem.INT("Eine bekannte Bedingung.")]]),
        "enabled_actions": Elem.ARRAY("Aktuell ausführbare Aktionen (Union-Tags der Aktion einer Regel aus {{{ref:automation/config}}})", members=[
            * 15 * [Elem.INT("Eine bekannte Bedingung.")]]),
    })),
    Func("config", FuncType.CONFIGURATION, Elem.OBJECT("Die Konfiguration der Automatisierung.", members={
            "tasks": Elem.ARRAY("Konfigurierte Regeln", members=[
                * 14 * [Elem.OBJECT("Eine Automatisierungsregel", members = {
                    "trigger": Elem.UNION("Bedingung, die zutreffen muss, damit Aktion ausgeführt wird", members={
                        0: Elem.NULL("Keine Bedingung konfiguriert."),
                        1: Elem.OBJECT("Zu einem bestimmten Zeitpunkt.", members={
                            "mday": Elem.INT("Tag des Monats (1 bis 31 oder -1, 0, 32)", constants=[
                                Const(-1, "Jeder Tag des Monats"),
                                Const(0, "Jeder Tag des Monats"),
                                Const(32, "Letzter Tag des Monats")
                            ]),
                            "wday": Elem.INT("Wochentag", constants=[
                                Const(-1, "Jeder Tag der Woche"),
                                Const(0, "Sonntag"),
                                Const(1, "Montag"),
                                Const(2, "Dienstag"),
                                Const(3, "Mittwoch"),
                                Const(4, "Donnerstag"),
                                Const(5, "Freitag"),
                                Const(6, "Samstag"),
                                Const(7, "Sonntag"),
                                Const(8, "Wochentags (Montag bis Freitag)"),
                                Const(9, "Am Wochenende (Samstag und Sonntag)"),
                            ]),
                            "hour": Elem.INT("Stunde des Tages (0 bis 23 oder -1)", constants=[
                                Const(-1, "Stündlich"),
                            ]),
                            "minute": Elem.INT("Minute des Tages (0 bis 59 oder -1)", constants=[
                                Const(-1, "Minütlich"),
                            ])
                        }),
                        2: Elem.OBJECT("Wechsel des Ladestatus", version=Version.CHARGER, members={
                            "old_charger_state": Elem.INT("Ladestatus vor dem Übergang", constants=[
                                Const(-1, "Beliebiger Ladestatus"),
                                Const(0, "Fahrzeug getrennt"),
                                Const(1, "Warte auf Freigabe"),
                                Const(2, "Ladebereit"),
                                Const(3, "Lädt"),
                                Const(4, "Fehler")
                            ]),
                            "new_charger_state": Elem.INT("Ladestatus nach dem Übergang", constants=[
                                Const(-1, "Beliebiger Ladestatus"),
                                Const(0, "Fahrzeug getrennt"),
                                Const(1, "Warte auf Freigabe"),
                                Const(2, "Ladebereit"),
                                Const(3, "Lädt"),
                                Const(4, "Fehler")
                            ]),
                        }),
                        3: Elem.OBJECT("Empfang einer MQTT-Nachricht", members={
                            "topic": Elem.STRING("MQTT-Topic-Filter, mit dem auf Nachrichten gewartet werden soll."),
                            "payload": Elem.STRING("Payload, der in der Nachricht enthalten sein soll"),
                            "retain": Elem.BOOL("Gibt an, ob auf retained-Pakete reagiert werden soll"),
                            "use_prefix": Elem.BOOL("Gibt an, ob der konfigurierte Global-Topic-Prefix (siehe {{{ref:mqtt/config}}}) vor dem konfigurierten Topic vorangestellt werden soll.")
                        }),
                        4: Elem.NULL("Drücken des Fronttasters", version=Version.WARP2 | Version.WARP3),
                        5: Elem.OBJECT("Erkennen eines NFC-Tags", version=Version.CHARGER, members={
                            "tag_type": Elem.INT("Typ des Tags", constants=[
                                Const(0, "Mifare Classic"),
                                Const(1, "NFC Forum Typ 1"),
                                Const(2, "NFC Forum Typ 2"),
                                Const(3, "NFC Forum Typ 3"),
                                Const(4, "NFC Forum Typ 4"),
                            ]),
                            "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
                        }),
                        6: Elem.NULL("Erreichen des Ladezeit- oder Energie-Limits", version=Version.CHARGER),
                        7: Elem.OBJECT("Schalten des Abschalteingangs", version=Version.WARP2 | Version.WARP3, members={
                            "high": Elem.BOOL("Gibt an, ob bei geöffnetem oder geschlossenem Eingang reagiert werden soll", constants=[
                                Const(True, "Reagieren bei geöffnetem Eingang"),
                                Const(False, "Reagieren bei geschlossenem Eingang"),
                            ])
                        }),
                        8: Elem.OBJECT("Schalten des konfigurierbaren Eingangs", version=Version.WARP2, members={
                            "high": Elem.BOOL("Gibt an, ob bei geöffnetem oder geschlossenem Eingang reagiert werden soll", constants=[
                                Const(True, "Reagieren bei geöffnetem Eingang"),
                                Const(False, "Reagieren bei geschlossenem Eingang"),
                            ])
                        }),
                        9: Elem.NULL("Auslösen des Watchdogs der externen Steuerung. Der Watchdog löst aus, wenn die externe Steuerung aktiv ist und {{{ref:evse/external_current_update}}} mindestens 30 Sekunden lang nicht aufgerufen wurde. ", version=Version.CHARGER),
                        10: Elem.NULL("Erkennen eines Fehlers durch die Zählerüberwachung", version=Version.CHARGER),
                        11: Elem.NULL("Auslösen des Watchdogs des Lastmanagements. Siehe {{{ref:charge_manager/config}}}"),
                        12: Elem.OBJECT("Schalten von Eingang 3", version=Version.WARPEM, members={
                            "state": Elem.BOOL("Gibt an, ob bei geöffnetem oder geschlossenem Eingang reagiert werden soll", constants=[
                                Const(True, "Reagieren bei geöffnetem Eingang"),
                                Const(False, "Reagieren bei geschlossenem Eingang"),
                            ])
                        }),
                        13: Elem.OBJECT("Schalten von Eingang 4", version=Version.WARPEM, members={
                            "state": Elem.BOOL("Gibt an, ob bei geöffnetem oder geschlossenem Eingang reagiert werden soll", constants=[
                                Const(True, "Reagieren bei geöffnetem Eingang"),
                                Const(False, "Reagieren bei geschlossenem Eingang"),
                            ])
                        }),
                        14: Elem.OBJECT("Schalten der Phasenumschaltung", version=Version.WARPEM, members={
                            "phase": Elem.INT("Gibt an, ob beim Umschalten auf ein- oder dreiphasig reagiert werden soll", constants=[
                                Const(1, "Reagieren beim Wechsel auf einphasig"),
                                Const(3, "Reagieren beim Wechsel auf dreiphasig"),
                            ])
                        }),
                        15: Elem.OBJECT("Erkennen eines Fehlers durch die Schützüberwachung", version=Version.WARPEM, members={
                            "contactor_okay": Elem.BOOL("Gibt an, ob reagiert werden soll, wenn ein oder kein Schützfehler vorliegt.", constants=[
                                Const(True, "Reagieren wenn ein Schützfehler erkannt wurde"),
                                Const(False, "Reagieren wenn kein Schützfehler erkannt wurde"),
                            ])
                        }),
                        16: Elem.OBJECT("Strom verfügbar TODO", version=Version.WARPEM, members={
                            "power_available": Elem.BOOL("Gibt an, ob reagiert werden soll, wenn Strom verfügbar, oder nicht verfügbar ist.", constants=[
                                Const(True, "Reagieren wenn Strom verfügbar ist"),
                                Const(False, "Reagieren wenn kein Strom verfügbar ist"),
                            ])
                        }),
                        17: Elem.OBJECT("Netzbezug- oder Einspeisung gemessen", version=Version.WARPEM, members={
                            "drawing_power": Elem.BOOL("Gibt an, ob reagiert werden soll, wenn Strom ins Netz eingespeist, oder aus dem Netz bezogen wird.", constants=[
                                Const(True, "Reagieren wenn Strom bezogen wird"),
                                Const(False, "Reagieren wenn Strom eingespeist wird"),
                            ])
                        }),
                    }),
                    "action": Elem.UNION("Aktion, die ausgeführt werden soll", members={
                        0: Elem.NULL("Keine Aktion konfiguriert."),
                        1: Elem.OBJECT("Schreibe ins Ereignislog", members={
                            "message": Elem.STRING("Nachricht, die ins Ereignislog geschrieben werden soll")
                        }),
                        2: Elem.OBJECT("Sende eine MQTT-Nachricht", members={
                            "topic": Elem.STRING("MQTT-Topic, an das die Nachricht gesendet werden soll."),
                            "payload": Elem.STRING("Payload, der in der Nachricht enthalten sein soll"),
                            "retain": Elem.BOOL("Gibt an, ob die Nachricht retained werden soll"),
                            "use_prefix": Elem.BOOL("Gibt an, ob der konfigurierte Global-Topic-Prefix (siehe {{{ref:mqtt/config}}}) vor dem konfigurierten Topic vorangestellt werden soll.")
                        }),
                        3: Elem.OBJECT("Limitiere den Ladestrom", version=Version.CHARGER, members={
                            "current": Elem.INT("Ladestromlimit, dass gesetzt werden soll")
                        }),
                        4: Elem.OBJECT("Zeige auf der Fronttaster-LED an", version=Version.CHARGER, members={
                            "state": Elem.INT("Blinkmuster, dass angezeigt werden soll.", constants=[
                                Const(-1, "EVSE kontrolliert LED"),
                                Const(0, "Aus"),
                                Const("1..254", "Per PWM gedimmtes leuchten"),
                                Const(255, "An"),
                                Const(1001, "Bestätigendes Blinken (z.B: NFC-Tag wurde erkannt)"),
                                Const(1002, "Ablehnendes Blinken (z.B: NFC-Tag ist unbekannt)"),
                                Const(1003, "Aufforderndes Blinken (z.B: NFC-Tag wird zum Laden benötigt)"),
                                Const("2001..2010", "Fehler-Blinken 1 bis 10."),
                            ]),
                            "duration": Elem.INT("Dauer für die der gesetzte Zustand erhalten bleibt.", unit=Units.ms)
                        }),
                        5: Elem.OBJECT("Setze einen Stromzähler zurück", members={
                            "meter_slot": Elem.INT("Meter-Slot-ID des Zählers, der zurückgesetzt werden soll")
                        }),
                        6: Elem.OBJECT("Setze den für den Lastmanager verfügbaren Strom.", members={
                            "current": Elem.INT("Verfügbarer Strom, der gesetzt werden soll")
                        }),
                        7: Elem.OBJECT("Simuliere ein NFC-Tags", version=Version.CHARGER, members={
                            "tag_type": Elem.INT("Typ des Tags.", constants=[
                                Const(0, "Mifare Classic"),
                                Const(1, "NFC Forum Typ 1"),
                                Const(2, "NFC Forum Typ 2"),
                                Const(3, "NFC Forum Typ 3"),
                                Const(4, "NFC Forum Typ 4"),
                            ]),
                            "tag_id": Elem.STRING("ID des Tags. Je nach Tag-Typ bis zu 10 Hex-Bytes, separiert durch ':'. z.B. 01:23:ab:3d"),
                            "tag_action": Elem.INT("Gibt an ob das Tag nur zum Starten oder Stoppen eines Ladevorgangs, oder für beides genutzt werden soll", constants=[
                                Const(0, "Tag kann Ladevorgänge starten und stoppen"),
                                Const(0, "Tag kann Ladevorgänge starten"),
                                Const(0, "Tag kann Ladevorgänge stoppen"),
                            ])
                        }),
                        8: Elem.OBJECT("Setze das Ladezeit- oder Energielimit", version=Version.CHARGER, members={
                            "restart": Elem.BOOL("Gibt an, ob die neuen Limits relativ zum bestehenden Ladevorgang, oder absolut gelten sollen. Wenn beispielsweise ein Ladevorgang seit 17 Minuten läuft und diese Aktion mit duration = 2 (30 Minuten) ausgelöst wird, dann darf, wenn restart false ist, der Ladevorgang noch weitere 13 Minuten laufen, sodass insgesamt 30 Minuten geladen wurde. Wenn restart true ist, darf weitere 30 Minuten, insgesamt also 47 Minuten geladen werden.", constants=[
                                Const(False, "Neues Ladelimit gilt relativ zum laufenden Ladevorgang. Z.B. Verlängerung <strong>auf</strong> 30 Minuten."),
                                Const(True, "Neues Ladelimit gilt absolut. Z.B. Verlängerung <strong>um</strong> 30 Minuten.")
                            ]),
                            "duration": Elem.INT("Zeitlimit eines Ladevorgangs. Nach Ablaufen des Zeitlimits wird der Ladevorgang gestoppt.", constants=[
                                Const(-1, "Zeitlimit nicht verändern"),
                                Const(0, "Unbegrenzt"),
                                Const(1, "15 Minuten"),
                                Const(2, "30 Minuten"),
                                Const(3, "45 Minuten"),
                                Const(4, "1 Stunde"),
                                Const(5, "2 Stunden"),
                                Const(6, "3 Stunden"),
                                Const(7, "4 Stunden"),
                                Const(8, "6 Stunden"),
                                Const(9, "8 Stunden"),
                                Const(10, "12 Stunden"),
                            ]),
                            "energy_wh": Elem.INT("Energielimit eines Ladevorgangs. Nach Ablaufen des Energielimits wird der Ladevorgang gestoppt.", unit=Units.Wh, constants=[
                                Const(-1, "Energielimit nicht verändern")
                            ]),
                        }),
                        9: Elem.OBJECT("Schalte den konfigurierbaren Ausgang", version=Version.WARP2, members={
                            "state": Elem.INT("Gibt an, ob der konfigurierte Ausgang geschlossen oder geöffnet werden soll.", constants=[
                                Const(0, "Geschlossen (verbunden mit Masse)"),
                                Const(1, "Geöffnet (hochohmig)"),
                            ])
                        }),
                        #10: Elem.OBJECT("Lösche die aufgezeichneten Ladevorgänge", version=Version.CHARGER, members={}),
                        11: Elem.OBJECT("Starte eine Phasenumschaltung", version=Version.WARPEM, members={
                            "phase": Elem.INT("Gibt an, auf ein- oder dreiphasig umgeschalted werden soll", constants=[
                                Const(1, "Wechsele auf einphasig"),
                                Const(3, "Wechsele auf dreiphasig"),
                            ])
                        }),
                        12: Elem.OBJECT("Wechsle den Lademodus", version=Version.WARPEM, members={
                            "mode": Elem.INT("Gewünschter Lademodus. Siehe {{{ref:power_manager/charge_mode}}}", constants=[
                                Const(0, "Schnell"),
                                Const(1, "Aus"),
                                Const(2, "PV"),
                                Const(3, "Min + PV"),
                            ])
                        }),
                        13: Elem.OBJECT("Schalte den Relais-Ausgang", version=Version.WARPEM, members={
                            "state": Elem.BOOL("Gibt an, ob der Relais-Ausgang geschlossen oder geöffnet werden soll.", constants=[
                                Const(True, "Geschlossen"),
                                Const(False, "Geöffnet"),
                            ])
                        }),
                        14: Elem.OBJECT("Limitiere den ???TODO???-Strom", version=Version.WARPEM, members={
                            "current": Elem.INT("Stromlimit, dass gesetzt werden soll", constants=[
                                Const(-1, "Stromlimit aufheben")
                            ])
                        }),
                        15: Elem.OBJECT("Blockiere oder gebe Ladevorgänge frei", version=Version.WARPEM, members={
                            "slot": Elem.INT("Blockierslot, der verwendet werden soll. Ladevorgänge werden nur dann erlaubt, wenn alle 4 Blockierslots nicht blockieren."),
                            "block": Elem.BOOL("Gibt an, ob der gewählte Blockierslot blockiert, oder freigegeben werden soll", constants=[
                                Const(False, "Gib gewählten Blockierslot frei"),
                                Const(True, "Blockiere gewählten Blockierslot")
                            ])
                        }),
                    }),
                })]
            ])
        })
    ),
])
