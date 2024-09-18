/** @odoo-module **/
import core from 'web.core';
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var rpc = require('web.rpc');
var session = require('web.session');

const SystrayWidget = Widget.extend({
    template: 'systray_icon',
    events: {
        'click .toggle-icon': '_onClick',
    },

    start: function () {
        this._super.apply(this, arguments);
        this._alwaysActivate();
    },

    _alwaysActivate: function () {
        var self = this;

        // RPC call to fetch data from shipment.delivery.terms
        rpc.query({
            model: 'shipment.delivery.terms',
            method: 'search_read',
            args: [[]],  // Fetch all records
            fields: [
                'id',
                'notify'
            ],
        }).then(function (result) {
            const allNotifyFalse = result.every(record => !record.notify);
            const dot = document.querySelector('.dot');

            if (allNotifyFalse) {
                if (dot) dot.style.display = 'none';
            } else {
                if (dot) dot.style.display = 'inline-block';
            }
        }).catch(function (error) {
            console.log('Error in RPC call:', error);
        });
    },

_onClick: function (ev) {
    ev.preventDefault();
    var self = this;

    const shipmentModeMap = {
        'aw': 'AW',
        'bl': 'BL',
        'bm': 'BM',
    };

    // Fetch updated data from shipment.delivery.terms
    rpc.query({
        model: 'shipment.delivery.terms',
        method: 'search_read',
        args: [[]],
        fields: [
            'id',
            'product_code',
            'product_id',
            'shipment_mode',
            'aw_bl_no',
            'aw_bl_date',
            'etd',
            'eta',
            'delivery_status',
            'shipment_term_id',
            'done',
            'notify',
            'form_id',
            'name'
        ],
    }).then(function (result) {
        console.log('Fetched records:', result);
        const dot = document.querySelector('.dot');
        const tbody = document.getElementById('shipment_data_tbody');
        const filteredRecords = result.filter(record => record.notify);

        console.log('Filtered records (notify = true):', filteredRecords);

        tbody.innerHTML = '';

        if (filteredRecords.length > 0) {
            dot.style.display = 'inline-block';

            filteredRecords.forEach(function (record) {
                const row = document.createElement('tr');

                row.appendChild(createTableCell(record.product_code || ''));
                row.appendChild(createTableCell(record.product_id ? record.product_id[1] : ''));
                row.appendChild(createTableCell(shipmentModeMap[record.shipment_mode] || record.shipment_mode || ''));
                row.appendChild(createTableCell(record.aw_bl_no || ''));
                row.appendChild(createTableCell(record.aw_bl_date || ''));
                row.appendChild(createTableCell(record.etd || ''));
                row.appendChild(createTableCell(record.eta || ''));

                row.addEventListener('click', function () {
                    self._onRowClick(record.id, record.shipment_term_id ? record.shipment_term_id[0] : null);
                });

                tbody.appendChild(row);
            });

            console.log('Updated table rows:', filteredRecords);

            // Prepare updated values and call Python method
            filteredRecords.forEach(function (record) {
                const updated_values = {
                    'product_code': { 'new_value': record.product_code },
                    'product_id': { 'new_value': record.product_id ? record.product_id[1] : '' },
                    'shipment_mode': { 'new_value': shipmentModeMap[record.shipment_mode] || record.shipment_mode },
                    'aw_bl_no': { 'new_value': record.aw_bl_no },
                    'aw_bl_date': { 'new_value': record.aw_bl_date },
                    'etd': { 'new_value': record.etd },
                    'eta': { 'new_value': record.eta },
                };

                // Log the updated values for inspection
                console.log('Updated Values:', updated_values);

                // Trigger RPC call to log only changed values
         rpc.query({
    model: 'fetch.data',
    method: 'create_fetch_data',
    args: [{
        updated_values: updated_values
    }]
}).then(function (result) {
    console.log("Python method 'create_fetch_data' executed successfully", result);
}).catch(function (error) {
    console.log("Error while calling 'create_fetch_data':", error);
});

            });

        } else {
            dot.style.display = 'none';
        }
    }).catch(function (error) {
        console.log('Error in RPC call:', error);
        const dot = document.querySelector('.dot');
        dot.style.display = 'none';
    });

    // Toggle dropdown visibility
    let dropBox = $(ev.currentTarget).closest('.new_icon').find('#systray_notif');
    if (dropBox.length > 0) {
        if (dropBox.is(':visible')) {
            dropBox.hide();
            $(document).off('click.systrayWidget');
        } else {
            dropBox.show();
            $(document).on('click.systrayWidget', function (e) {
                if (!$(e.target).closest('.new_icon').length) {
                    dropBox.hide();
                    $(document).off('click.systrayWidget');
                }
            });
        }
    }
},



_onRowClick: function (recordId, shipmentTermId) {
    var self = this;

    // Step 1: Update the record to set notify to false
    rpc.query({
        model: 'shipment.delivery.terms',
        method: 'write',
        args: [[recordId], { notify: false }],
    }).then(function (response) {
        console.log('Record updated:', response);

        // Step 2: Fetch updated record details
        return rpc.query({
            model: 'shipment.delivery.terms',
            method: 'search_read',
            args: [[['id', '=', recordId]], 0, 1], // Correct domain format: [['field', 'operator', value]]
            fields: [
                'id',
                'product_code',
                'product_id',
                'shipment_mode',
                'aw_bl_no',
                'aw_bl_date',
                'etd',
                'eta',
                'delivery_status',
                'shipment_term_id',
                'done',
                'notify',
                'form_id',
                'name'
            ],
        });
    }).then(function (updatedResult) {
        const tbody = document.getElementById('shipment_data_tbody');
        tbody.innerHTML = '';

        // Populate the table with updated data
        updatedResult.forEach(function (record) {
            const row = document.createElement('tr');

            row.appendChild(createTableCell(record.product_code || ''));
            row.appendChild(createTableCell(record.product_id ? record.product_id[1] : ''));
            row.appendChild(createTableCell(record.shipment_mode === 'aw' ? 'AW' : 'BL'));
            row.appendChild(createTableCell(record.aw_bl_no || ''));
            row.appendChild(createTableCell(record.aw_bl_date || ''));
            row.appendChild(createTableCell(record.etd || ''));
            row.appendChild(createTableCell(record.eta || ''));

            tbody.appendChild(row);
        });
    }).catch(function (error) {
        console.log('Error:', error);
    });

    // Redirect if shipmentTermId is available
    if (shipmentTermId) {
        window.location.href = `${session.url('/web?#model=sale.order.delivery&id=' + shipmentTermId + '&view_type=form')}`;
    } else {
        console.log('Error: shipmentTermId is missing');
    }
},
});

function createTableCell(text) {

    const cell = document.createElement('td');
    cell.textContent = text;
    cell.style.padding = '10px';
    cell.style.borderBottom = '1px solid #eee';
    return cell;

}

SystrayMenu.Items.push(SystrayWidget);

export default SystrayWidget;
