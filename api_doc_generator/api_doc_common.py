from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Union, Optional
import itertools

def wrap_non_empty(prefix, middle, suffix):
    if len(middle) == 0:
        return ''

    return prefix + middle + suffix

@dataclass
class Unit:
    name: str
    abbr: str

    def to_html(self):
        return '(<abbr title="{}">{}</abbr>)'.format(self.name, self.abbr)

class Units:
    A = Unit("Ampere", "A")
    Ah = Unit("Amperestunde", "Ah")
    degree = Unit("Grad", "°")
    Hz = Unit("Hertz", "Hz")
    kVAh = Unit("Kilovoltamperestunde", "kVAh")
    kvarh = Unit("Kilovoltampere Reaktiv Stunde", "kvarh")
    kWh = Unit("Kilowattstunde", "kWh")
    mA = Unit("Milliampere", "mA")
    ms = Unit("Millisekunde", "ms")
    mV = Unit("Millivolt", "mV")
    Mbps = Unit("Megabit pro Sekunde", "Mbit/s")
    ohm = Unit("Ohm", "Ω")
    percent = Unit("Prozent", "%")
    tenth_percent = Unit("Zehntel Prozent", "%/10")
    V = Unit("Volt", "V")
    VA = Unit("Voltampere", "VA")
    var = Unit("Voltampere Reaktiv", "var")
    W = Unit("Watt", "W")

class FuncType(IntEnum):
    STATE = 0
    COMMAND = 1
    CONFIGURATION = 2
    HTTP_ONLY = 3

    def name_singular(self):
        return {
            FuncType.STATE: "Zustand",
            FuncType.COMMAND: "Kommando",
            FuncType.CONFIGURATION: "Konfiguration",
            FuncType.HTTP_ONLY: "HTTP-Spezifisch"
        }[self]

    def name_plural(self):
        return {
            FuncType.STATE: "Zustände",
            FuncType.COMMAND: "Kommandos",
            FuncType.CONFIGURATION: "Konfigurationen",
            FuncType.HTTP_ONLY: "HTTP-Spezifisch"
        }[self]

@dataclass
class Func:
    name: str
    type_: FuncType
    root: 'Elem'
    command_is_action: bool = False

class EType(IntEnum):
    OBJECT = 0
    ARRAY = 1
    STRING = 2
    INT = 3
    FLOAT = 4
    BOOL = 5
    NULL = 6
    OPAQUE = 7

class Version(IntEnum):
    ANY = 0
    WARP1_ONLY = 1
    WARP2_ONLY = 2

@dataclass
class Const:
    val: str
    desc: str
    version: Version = Version.ANY

@dataclass
class Elem:
    type_: EType
    desc: str
    unit: Optional[Unit]
    val: Optional[Union[list['Elem'], dict[str, 'Elem']]]
    constants: Optional[list[Const]]
    is_var_length_array: bool
    var_length_array_type: Optional[EType]
    var_length_array_unit: Optional[Unit]
    censored: bool
    version: Version

    @staticmethod
    def OBJECT(desc: str, *, members: dict[str, 'Elem'], censored: bool = False, version: Version = Version.ANY):
        return Elem(EType.OBJECT, desc, None, members, None, False, None, None, censored, version)

    @staticmethod
    def ARRAY(desc: str, *, unit: Optional[Unit] = None, members: Optional[list['Elem']] = None, member_type: Optional[EType] = None, member_unit: Optional[Unit] = None, censored: bool = False, version: Version = Version.ANY):
        if members is None and member_type is None:
            raise Exception("Array without members and member_type is not supported!")
        if members is not None and member_type is not None and any(x.type_ != member_type for x in members):
            raise Exception("Type mismatch between members and member_type!")
        return Elem(EType.ARRAY, desc, unit, members, None, members is None, member_type, member_unit, censored, version)

    @staticmethod
    def STRING(desc: str, *, constants: Optional[list[Const]] = None, censored: bool = False, version: Version = Version.ANY):
        return Elem(EType.STRING, desc, None, None, constants, False, None, None, censored, version)

    @staticmethod
    def INT(desc: str, *, unit: Optional[Unit] = None, constants: Optional[list[Const]] = None, censored: bool = False, version: Version = Version.ANY):
        return Elem(EType.INT, desc, unit, None, constants, False, None, None, censored, version)

    @staticmethod
    def FLOAT(desc: str, *, unit: Optional[Unit] = None, constants: Optional[list[Const]] = None, censored: bool = False, version: Version = Version.ANY):
        return Elem(EType.FLOAT, desc, unit, None, constants, False, None, None, censored, version)

    @staticmethod
    def BOOL(desc: str, *, constants: Optional[list[Const]] = None, censored: bool = False, version: Version = Version.ANY):
        return Elem(EType.BOOL, desc, None, None, constants, False, None, None, censored, version)

    @staticmethod
    def NULL(desc: str):
        return Elem(EType.NULL, desc, None, None, None, False, None, None, False, Version.ANY)

    @staticmethod
    def OPAQUE(desc: str):
        return Elem(EType.OPAQUE, desc, None, None, None, False, None, None, False, Version.ANY)

    def get_type(self) -> str:
        if self.type_ in (EType.OBJECT,
                          EType.STRING,
                          EType.INT,
                          EType.FLOAT,
                          EType.BOOL):
            return self.type_.name.lower()

        if self.type_ == EType.ARRAY:
            if self.is_var_length_array:
                return self.var_length_array_type.name.lower() + "[..]"

            if len(set([x.version for x in self.val])) > 1:
                return self.val[0].get_type() + "[..]"

            return self.val[0].get_type() + "[{}]".format(len(self.val))

        if self.type_ == EType.OBJECT:
            return "object"

    def get_unit(self) -> str:
        if self.type_ in (EType.OBJECT,
                          EType.STRING,
                          EType.INT,
                          EType.FLOAT,
                          EType.BOOL):
            return self.unit.to_html() if self.unit is not None else ''

        if self.type_ == EType.ARRAY:
            if self.is_var_length_array:
                return self.var_length_array_unit.to_html() if self.var_length_array_unit is not None else ''

            if all(x.get_unit() == '' for x in self.val):
                return self.unit.to_html() if self.unit is not None else ''

            if len(set([x.get_unit() for x in self.val])) == len(self.val):
                return self.val[0].get_unit()

            print("Warning: Array with more than one unit found! Those units will not be documented")
            return ''

        if self.type_ == EType.OBJECT:
            return ''

    def to_html(self, key_name) -> str:
        row_template = """
<tr class="{version_class}">
    <th scope="row">{name}</th>
    <td>{version_prefix}{desc}</td>
</tr>"""

        constants_template = """
<div class="{version_class}">
{version_label}<ol class="ol-enum">
    {entries}
</ol>
</div>"""
        constant_entry_template = """<li>{val} - {desc}</li>"""

        name = '{name}<br/><span class="th-details">{type}{unit}</span>'.format(
                    name=key_name,
                    type=self.get_type(),
                    unit=wrap_non_empty(' ', self.get_unit(), ''))

        desc = self.desc

        if self.constants is not None:
            for version, constants in itertools.groupby(sorted(self.constants, key=lambda c: c.version), key=lambda c: c.version):
                consts = []
                for c in constants:
                    val = c.val
                    if self.type_ == EType.BOOL:
                        val = str(val).lower()
                    consts.append(constant_entry_template.format(val="<strong>{}</strong>".format(val), desc=c.desc))

                if len(consts) == 0:
                    continue

                desc += constants_template.format(version_class= version.name.lower(),
                                                  version_label={Version.ANY:"", Version.WARP1_ONLY: "<strong>WARP 1:</strong><br>", Version.WARP2_ONLY: "<strong>WARP 2:</strong><br>"}[version],
                                                  entries='\n    '.join(consts))

        if self.type_ == EType.ARRAY and self.val is not None:
            # Python has no break with labels. Use function with return to "break" out of the outer loop
            def get_desc(desc):
                result = desc
                for version, members in itertools.groupby(sorted(self.val, key=lambda c: c.version), key=lambda c: c.version):
                    members = list(members)
                    mems = []
                    idx = 0
                    for m, elements in itertools.groupby(members):
                        count = len(list(elements))
                        d = m.desc
                        # If the whole array is composed of identical entries without description, skip the whole list. This is used for example in IPs.
                        if d == "":
                            if count == len(members):
                                return result

                        if m.type_ == EType.OBJECT:
                            d += m.to_html_table(False)
                        mems.append(constant_entry_template.format(val="[{}]".format(idx) if count == 1 else "[{}..{}]".format(idx, idx + count - 1), desc=d))
                        idx += count

                    if len(mems) == 0:
                        continue

                    result += constants_template.format(version_class= version.name.lower(),
                                                    version_label={Version.ANY:"", Version.WARP1_ONLY: "<strong>WARP 1:</strong><br>", Version.WARP2_ONLY: "<strong>WARP 2:</strong><br>"}[version],
                                                    entries='\n    '.join(mems))
                return result
            desc = get_desc(desc)

        if self.type_ == EType.OBJECT:
            desc += self.to_html_table(is_root=False)

        return row_template.format(version_class=self.version.name.lower(),
                                   name=name,
                                   version_prefix={Version.ANY:"", Version.WARP1_ONLY: "<strong>(Nur WARP 1)</strong> ", Version.WARP2_ONLY: "<strong>(Nur WARP 2)</strong> "}[self.version],
                                   desc=desc)

    def root_to_html(self, f: Func, module: str) -> str:
        template = """
<div class="{version_class}">
    <div class="h5" id="{fn_id}">{fn_path}{version_text}</div>
    {fn_desc}{fn_table}
</div>"""

        if self.type_ == EType.NULL:
            table = "<br/><strong>Leerer Payload. Es muss null übergeben werden.</strong>"
            if f.type_ != FuncType.COMMAND:
                print("Function {} has a null payload but is not a command?!?".format(f.name))
            elif f.command_is_action:
                table += "<br/><strong>Löst eine einmalige Aktion aus. Nachrichten, die über den Broker retained wurden, werden ignoriert.</strong>"
        else:
            table = self.to_html_table(is_root=True)

        return template.format(fn_id = module + "_" + f.name if module is not None else f.name,
                               fn_path = module + "/" + f.name if module is not None else f.name,
                               fn_desc = self.desc,
                               fn_table = table,
                               version_class=self.version.name.lower(),
                               version_text={Version.ANY:"", Version.WARP1_ONLY: " <strong>(Nur WARP 1)</strong> ", Version.WARP2_ONLY: " <strong>(Nur WARP 2)</strong> "}[self.version])

    def to_html_table(self, is_root) -> str:
        table_template = """
<div class="table-responsive">
    <table class="table {striped} table-bottom-border mt-3">
        <thead class="thead-dark">
            <tr>
            <th scope="col" style="width: 25%">{name_or_index}</th>
            <th scope="col">Bedeutung</th>
            </tr>
        </thead>
        <tbody>
{rows}
        </tbody>
    </table>
</div>"""

        striped = "table-striped" if is_root else "table-not-striped mt-3"

        if self.type_ == EType.OBJECT:
            return table_template.format(name_or_index="Name", striped=striped, rows='\n'.join([v.to_html(k) for k, v in self.val.items()]))

        if self.type_ == EType.ARRAY:
            idx = 0
            rows = []
            for group, elements in itertools.groupby(self.val):
                count = len(list(elements))
                rows.append(group.to_html("[{}]".format(idx) if count == 1 else "[{}..{}]".format(idx, idx + count - 1)))
                idx += count

            return table_template.format(name_or_index="Index", striped=striped, rows='\n'.join(rows))

        if self.type_ == EType.OPAQUE:
            return ""

        print("primitive roots not implemented yet!")
        return None


@dataclass
class Module:
    name: str
    display_name: str
    desc: str
    version: Version
    functions: list[Func]
    hide_prefix: bool = False

    def to_html(self) -> str:
        template = """<section id="reference-{name}" class="section {version}">
    <header class="reference-section-header">
        <h4>{display_name}{desc}</h4>
    </header>
    <ul class="ul-no-bullet">
        {toc}
    </ul>
    {functions}
</section>"""

        toc_group_template = """<li>
    {group_name}
    <ul>
        {links}
    </ul>
</li>"""

        toc = []
        functions = []

        for group, fns in itertools.groupby(self.functions, key=lambda f: f.type_):
            fns = list(fns)

            for f in fns:
                functions.append(f.root.root_to_html(f, self.name if not self.hide_prefix else None))

            toc.append(toc_group_template.format(
                group_name=group.name_plural(),
                links='\n'.join("<li>{{{ref:" + ("{}/{}".format(self.name, x.name) if not self.hide_prefix else x.name) + "}}}</li>" for x in fns)))


        return template.format(name=self.name,
                               desc=wrap_non_empty(" - ",self.desc,""),
                               display_name=self.display_name,
                               version=self.version.name.lower(),
                               toc="\n".join(toc),
                               functions="\n".join(functions))