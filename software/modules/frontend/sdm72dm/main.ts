import $ from "jquery";

import * as util from "../util";

import Chartist = require("chartist");
import ctAxisTitle = require("chartist-plugin-axistitle");

interface MeterStateEntry {
    total: number,
    import: number,
    export: number
}

interface MeterState {
    power: MeterStateEntry,
    energy_rel: MeterStateEntry,
    energy_abs: MeterStateEntry,
}

function update_meter_state(state: MeterState) {
    $('#meter_power_total').val(state.power.total.toFixed(0) + " W");
    $('#meter_power_import').val(state.power.import.toFixed(0) + " W");
    $('#meter_power_export').val(state.power.export.toFixed(0) + " W");

    $('#meter_energy_rel_total').val(state.energy_rel.total.toFixed(3) + " kWh");
    $('#meter_energy_rel_import').val(state.energy_rel.import.toFixed(3) + " kWh");
    $('#meter_energy_rel_export').val(state.energy_rel.export.toFixed(3) + " kWh");

    $('#meter_energy_abs_total').val(state.energy_abs.total.toFixed(3) + " kWh");
    $('#meter_energy_abs_import').val(state.energy_abs.import.toFixed(3) + " kWh");
    $('#meter_energy_abs_export').val(state.energy_abs.export.toFixed(3) + " kWh");
}


let live_interval: number = null;

function meter_chart_change_time(value: string) {
    if (live_interval != null) {
        clearInterval(live_interval);
        live_interval = null;
    }

    if (value == "live") {
        live_interval = setInterval(() =>
            $.get("/power_live").done(function (result) {
                let values = result["samples"];
                let sps = result["samples_per_second"];
                let labels = Array(values.length + 1).fill(null);

                let now = Date.now();
                let start = now - 1000 * values.length / sps;
                let last_minute = -1;
                for(let i = 0; i < labels.length; ++i) {
                    let d = new Date(start + i * (1000 * (1/sps)));
                    if(d.getSeconds() == 0 && d.getMinutes() != last_minute) {
                        labels[i] = d.toLocaleTimeString(navigator.language, {hour: '2-digit', minute: '2-digit', second: '2-digit'});
                        last_minute = d.getMinutes();
                    }
                }

                let data = {
                    labels: labels,
                    series: [
                        values
                    ]
                };
                meter_chart.update(data);
            }
            ), 1000);
        return;
    } else if (value == "history") {
        $.get("/power_history").done(function (values: Number[]) {
            const HISTORY_MINUTE_INTERVAL = 4;
            const VALUE_COUNT = 48 * (60 / HISTORY_MINUTE_INTERVAL);
            const LABEL_COUNT = 9;
            const VALUES_PER_LABEL = VALUE_COUNT / (LABEL_COUNT - 1); // - 1 for the last label that has no values

            if (values.length != VALUE_COUNT) {
                console.log("Unexpected number of values to plot!");
                return;
            }

            let labels = Array(values.length + 1).fill(null);

            let now = Date.now();
            let start = now - 1000 * 60 * 60 * 48;
            for(let i = 0; i < labels.length; i += VALUES_PER_LABEL) {
                let d = new Date(start + i * (1000 * 60 * HISTORY_MINUTE_INTERVAL));
                labels[i] = d.toLocaleTimeString(navigator.language, {hour: '2-digit', minute: '2-digit'});
            }

            let data = {
                labels: labels,
                series: [
                    values
                ]
            };
            meter_chart.update(data);
        });
    } else {
        console.log("Unknown plot type!");
    }
}

let meter_chart: Chartist.IChartistLineChart;

function init_chart() {
    let data = {};

    // Create a new line chart object where as first parameter we pass in a selector
    // that is resolving to our chart container element. The Second parameter
    // is the actual data object.
    meter_chart = new Chartist.Line('#meter_chart', data, {
        fullWidth: true,
        showPoint: false,
        axisX: {
            offset: 50,
            labelOffset: {x: 0, y: 5}
        },
        axisY: {
            scaleMinSpace: 40,
            onlyInteger: true,
            offset: 50,
            labelOffset: {x: 0, y: 6}
        },
        plugins: [
            ctAxisTitle({
                axisX: {
                axisTitle: "Time",
                axisClass: "ct-axis-title",
                offset: {
                    x: 0,
                    y: 40
                },
                textAnchor: "middle"
                },
                axisY: {
                axisTitle: "Power (Watt)",
                axisClass: "ct-axis-title",
                offset: {
                    x: 0,
                    y: 12
                },
                flipTitle: true
                }
            })
        ]
    });

    let input = <HTMLInputElement>document.getElementById("meter_chart_time_select");
    meter_chart_change_time(input.value);
}

function energy_meter_reset_statistics() {
    $.get("/energy_meter_reset").done(function () {
        util.show_alert("alert-success", "Energy data reset initiated.", "");
    });
}

export function init() {
    let input = <HTMLInputElement>document.getElementById("meter_chart_time_select");
    input.addEventListener(
        "change", () => meter_chart_change_time(input.value)
    );

    (<HTMLButtonElement>document.getElementById("energy_meter_reset_statistics_button")).addEventListener("click", energy_meter_reset_statistics);

    // The energy meter tab layout is generated when it is shown first.
    // We have to create the chart then, to make sure it is scaled correctly.
    // Immediately deregister afterwards, as we don't want to recreate the chart
    // every time.
    $('#sidebar-meter').on('shown.bs.tab', function (e) {
        init_chart();
    });

    $('#sidebar-meter').on('hidden.bs.tab', function (e) {
        if (live_interval != null) {
            clearInterval(live_interval);
            live_interval = null;
        }
    });
}

export function addEventListeners(source: EventSource) {
    source.addEventListener('meter_state', function (e: util.SSE) {
        update_meter_state(<MeterState>(JSON.parse(e.data)));
    }, false);
}

export function updateLockState(module_init) {
    $('#sidebar-meter').prop('hidden', !module_init.sdm72dm);
}
