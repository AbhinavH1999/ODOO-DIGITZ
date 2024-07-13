
/** @odoo-module **/
import core from 'web.core';
import SystrayMenu from 'web.SystrayMenu';
import Widget from 'web.Widget';
var qweb = core.qweb
var rpc = require('web.rpc');
console.log('hi')

const SystrayWidget = Widget.extend({
  template: 'IconSystrayDropdown',
  events: {
       'click .display_devel':'_onClick2',
      'click .display ':'_onClick1',
      'click .o-dropdown': '_onClick',
      'click #btn': '_changeButtonColor',

  },

  _onClick: function(ev){
       var self = this
       console.log('hi')
//       this._toggleDropdown(ev);

       rpc.query({
               model: 'sale.order',
               method: 'search_read',
               args:[]
//               fields:['name','customer','salesperson']
           })
//        this.$el.html(qweb.render('FieldSelectionBadge', {'values': this.values, 'current_value': this.currentValue}));

            .then(function (result){
            self.$('.systray_notification').html(qweb.render('SystrayDetails', {
                              Datas:result
                            }));
                            });



       let dropBox = $(ev.currentTarget.parentElement).find('#systray_notif')
       if (dropBox.length > 0 && dropBox[0].style.display == 'block'){

           dropBox[0].style.display = 'none'

       }
       else if (dropBox.length > 0) {
           dropBox[0].style.display = 'block'


       }
       $('.systray_notification').html(("SystrayDetails"))
  },
 _onClick1: function(ev){
       var self = this
       console.log('hi')

       console.log('fn ready')
       rpc.query({
               model: 'sale.order',
               method: 'search_read',
               args:[]
           })

            .then(function (result){
            self.$('.systray_notification').html(qweb.render('SystrayDetails', {
                              Data:result
                            }));
                            });



  },

    _onClick2: function(ev){
        var self = this
        console.log('helloo')


        rpc.query({
            model:  'hospital.patient',
            method: 'search_read',
            args:[]
        })
            .then(function (result){
            console.log(result)
            self.$('.systray_notification').html(qweb.render('SystrayDetails', {
                              value:result
                            }));
                            });



            },
 _changeButtonColor: function(ev) {
    ev.preventDefault();
    ev.stopPropagation();
    $('#btn').addClass('red-background'); // Add a CSS class to change button color
  }


});
           $(document).mouseup(function (e) {
            if ($(e.target).
                closest(".o_MessagingMenu").
                length=== 0) {
                $(".o_MessagingMenu_dropdownMenu.o-dropdown-menu").hide();
            }

            else  {
                $(".systray_notification").show();
                }
        });





SystrayMenu.Items.push(SystrayWidget);
export default SystrayWidget;





