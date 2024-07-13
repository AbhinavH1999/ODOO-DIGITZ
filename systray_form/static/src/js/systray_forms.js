
///** @odoo-module **/
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component, useState } from "@odoo/owl";
//import { Dropdown } from '@web/core/dropdown/dropdown';
//import { DropdownItem } from '@web/core/dropdown/dropdown_item';
//
//class SystrayIcon extends Component {
//    setup() {
//        super.setup(...arguments);
//        this.action = useService("action");
//        this.state = useState({ showBadge: false });
//    }
//
//    async _openSaleModel() {
//        await this.action.doAction({
//            type: "ir.actions.act_window",
//            name: "Systray form",
//            res_model: "systray.forms",
//            view_mode: "tree",
//            views: [[false, "tree"], [false, "form"]],
//            target: "current",
//        });
//        this.state.showBadge = true;
//
//
//    }
//}
//
//SystrayIcon.template = "systray_forms";
//SystrayIcon.components = { Dropdown, DropdownItem };
//export const systrayItem = { Component: SystrayIcon };
//registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });





/** @odoo-module **/
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component, useState } from "@odoo/owl";
//import { Dropdown } from '@web/core/dropdown/dropdown';
//import { DropdownItem } from '@web/core/dropdown/dropdown_item';
//import core from 'web.core';
//import SystrayMenu from 'web.SystrayMenu';
//import Widget from 'web.Widget';
//var qweb = core.qweb
//var rpc = require('web.rpc');
//
//class SystrayIcon extends Component {
//    setup() {
//        super.setup(...arguments);
//        this.action = useService("action");
//        this.state = useState({ showBadge: false });
//    }
//
//    _onClick() {
//          await rpc.query({
//        model: 'systray.forms',
//        method: 'my_python_function',
//        args: []
//        }).then(function(){
//        console.log("RPC call successful");
//    });
//        this.action.doAction({
//
//            type: "ir.actions.act_window",
//            name: "Systray Form",
//            res_model: "systray.forms",
//            view_mode: "tree,form",
//            views: [[false, "tree"], [false, "form"]],
//            target: "current",
//        });
////        this.state.showBadge = true;
//
//
//    }
//}
//
//SystrayIcon.template = "systray_forms.SystrayIcon";
//SystrayIcon.components = { Dropdown, DropdownItem };
//
//export const systrayItem = { Component: SystrayIcon };
//registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });



//

/** @odoo-module **/
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component, useState, onWillStart, onWillUnmount } from "@odoo/owl";
//import { Dropdown } from '@web/core/dropdown/dropdown';
//import { DropdownItem } from '@web/core/dropdown/dropdown_item';
//import rpc from 'web.rpc';
//
//class SystrayIcon extends Component {
//    setup() {
//        super.setup();
//        this.action = useService("action");
//        this.state = useState({ showBadge: false });
//
//        this.interval = null;
//        this.startInterval();
//    }
//
//    startInterval() {
//        this.interval = setInterval(async () => {
//            try {
//                const result = await rpc.query({
//                    model: 'systray.forms',
//                    method: 'my_python_function',
//                    args: [[]],
//                });
//                console.log('Python function called successfully:', result);
//
//                // Assuming `result` is an object that contains `check`
//                if (result.check === true) {
//                       this.state.showBadge = true;
//                    console.log('Badge should be shown now.');
//                } else {
//
//                    console.log('Badge should be hidden.');
//                }
//            } catch (error) {
//                console.error('Error while calling Python function:', error.message);
//                // Handle error if needed
//            }
//        }, 5000); // 5000 milliseconds = 5 seconds
//    }
//
//    async _onClick() {
//             if (this.state.showBadge) {
//            this.state.showBadge = false; // Hide the badge when the systray icon is clicked
//        }
//        try {
//            await this.action.doAction({
//                type: "ir.actions.act_window",
//                name: "Systray Form",
//                res_model: "systray.forms",
//                view_mode: "tree,form",
//                views: [[false, "tree"], [false, "form"]],
//                target: "current",
//            });
//        } catch (error) {
//            console.error('Error while performing action:', error.message);
//        }
//    }
//
//    willUnmount() {
//        if (this.interval) {
//            clearInterval(this.interval);
//        }                                                my code
//    }
//}
//
//SystrayIcon.template = "systray_forms.SystrayIcon";
//SystrayIcon.components = { Dropdown, DropdownItem };
//
//export const systrayItem = { Component: SystrayIcon };
//registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });
//
///** @odoo-module **/
//import { registry } from "@web/core/registry";
//import { useService } from "@web/core/utils/hooks";
//import { Component, useState, onWillStart, onWillUnmount } from "@odoo/owl";
//import { Dropdown } from '@web/core/dropdown/dropdown';
//import { DropdownItem } from '@web/core/dropdown/dropdown_item';
//import rpc from 'web.rpc';
//
//class SystrayIcon extends Component {
//    setup() {
//        super.setup();
//        this.action = useService("action");
//        this.state = useState({ showBadge: false, isAdmin: false });
//
//        this.interval = null;
//        this.startInterval();
//
//        this.checkAdmin();
//    }
//
//    async checkAdmin() {
//        try {
//            const result = await rpc.query({
//                model: 'res.users',
//                method: 'has_group',
//                args: ['systray_form.group_lunch_systray_manager'],
//            });
//            this.state.isAdmin = result;
//
//        } catch (error) {
//            console.error('Error while checking admin group:', error.message);
//        }
//    }
//
//    startInterval() {
//        this.interval = setInterval(async () => {
//            try {
//                const result = await rpc.query({
//                    model: 'systray.forms',
//                    method: 'my_python_function',
//                    args: [[]],
//                });
//                console.log('Python function called successfully:', result);
//
//                // Assuming `result` is an object that contains `check`
//                if (result.check === true) {
//                    this.state.showBadge = true;
//                    console.log('Badge should be shown now.');
//                } else {
//                    this.state.showBadge = false;
//                    console.log('Badge should be hidden.');
//                }
//            } catch (error) {
//                console.error('Error while calling Python function:', error.message);
//                // Handle error if needed
//            }
//        }, 3000); // 5000 milliseconds = 5 seconds
//    }
//
//    async _onClick() {
//        if (this.state.isAdmin && this.state.showBadge) {
//            this.state.showBadge = false; // Hide the badge when the systray icon is clicked if the user is admin
//        }
//        try {
//            await this.action.doAction({
//                type: "ir.actions.act_window",
//                name: "Systray Form",
//                res_model: "systray.forms",
//                view_mode: "tree,form",
//                views: [[false, "tree"], [false, "form"]],
//                target: "current",
//            });
//        } catch (error) {
//            console.error('Error while performing action:', error.message);
//        }
//    }
//
//    willUnmount() {
//        if (this.interval) {
//            clearInterval(this.interval);                      my code dont delete
//        }
//    }
//}
//
//SystrayIcon.template = "systray_forms.SystrayIcon";
//SystrayIcon.components = { Dropdown, DropdownItem };
//
//export const systrayItem = { Component: SystrayIcon };
//registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });

/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { Dropdown, DropdownItem } from '@web/core/dropdown/dropdown';
import rpc from 'web.rpc';

class SystrayIcon extends Component {
    setup() {
        super.setup();
        this.action = useService("action");
        this.state = useState({ showBadge: false, isAdmin: false });

        this.checkAdmin();
        this.startInterval();
    }

    async checkAdmin() {
        try {
            const result = await rpc.query({
                model: 'res.users',
                method: 'has_group',
                args: ['systray_form.group_lunch_systray_manager'],
            });
            this.state.isAdmin = result;
        } catch (error) {
            console.error('Error while checking admin group:', error.message);
        }
    }

    startInterval() {
        this.interval = setInterval(async () => {
            try {
                const result = await rpc.query({
                    model: 'systray.forms',
                    method: 'my_python_function',
                    args: [[]],
                });
                console.log('Python function called successfully:', result);

                // Assuming `result` is an object that contains `check`
                if (result.check === true) {
                    this.state.showBadge = true;
                    console.log('Badge should be shown now.');
                } else {
                    this.state.showBadge = false;
                    console.log('Badge should be hidden.');
                }
            } catch (error) {
                console.error('Error while calling Python function:', error.message);
                // Handle error if needed
            }
        }, 850); // Interval in milliseconds (3000 ms = 3 seconds)
    }

    async _onClick() {
        if (this.state.isAdmin) {
            if (this.state.showBadge) {
                this.state.showBadge = false; // Hide the badge when the systray icon is clicked if the user is admin
            }

            // Stop the interval when the admin clicks the systray icon
            if (this.interval) {
                clearInterval(this.interval);
                this.interval = null;
            }

            // Call RPC to set `check=false`
            try {
                await rpc.query({
                    model: 'systray.forms',
                    method: 'set_check_false', // Replace with your method name
                    args: [[]],
                });
                console.log('RPC call to set check=false successful.');
            } catch (error) {
                console.error('Error while setting check=false:', error.message);
            }
        }

        // Always perform the action regardless of admin status
        try {
            await this.action.doAction({
                type: "ir.actions.act_window",
                name: "Systray Form",
                res_model: "systray.forms",
                view_mode: "tree,form",
                views: [[false, "tree"], [false, "form"]],
                target: "current",
            });
        } catch (error) {
            console.error('Error while performing action:', error.message);
        }
    }

    willUnmount() {
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
}

SystrayIcon.template = "systray_forms.SystrayIcon";
SystrayIcon.components = { Dropdown, DropdownItem };

export const systrayItem = { Component: SystrayIcon };
registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 1 });


