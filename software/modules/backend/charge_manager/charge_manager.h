/* warp-charger
 * Copyright (C) 2020-2021 Erik Fleckstein <erik@tinkerforge.com>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#pragma once

#include "config.h"

#include "async_http_client/AsyncHttpClient.h"

class ChargeManager {
public:
    ChargeManager();
    void setup();
    void register_urls();
    void post_setup();
    void loop();

    bool initialized = false;

private:
    void start_evse_state_update();
    void update_local_evse_state(Config *target);
    void send_current();
    void distribute_current();
    void update_local_current(Config *target);
    Config charge_manager_config;
    Config charge_manager_config_in_use;

    Config charge_manager_state;

    size_t current_charger;

    bool request_in_progress;
    uint32_t request_id;
    AsyncHttpClient client;
    String buf;
};
