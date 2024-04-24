odoo.define('hr_attendance_apexive.my_attendances', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var field_utils = require('web.field_utils');

    const session = require('web.session');
    MyAttendances.include({
        events: _.extend({}, MyAttendances.prototype.events, {
            'change #oe_project': 'OnChangeProject',
        }),

        willStart: function () {
            console.log('Test01')
            var self = this;
            console.log(self)
            var def = this._rpc({
                model: "hr.employee",
                method: "search_read",
                args: [[["user_id", "=", this.getSession().uid]], ["attendance_state", "name", "hours_today", "login_project_id", "login_task_id", "login_description"]],
                context: session.user_context,
            }).then(function (res) {
                self.employee = res.length && res[0];
                if (res.length) {
                    self.hours_today = field_utils.format.float_time(self.employee.hours_today);
                    if (self.employee.login_project_id) {
                        self.projectName = self.employee.login_project_id[1];
                    }
                    if (self.employee.login_task_id) {
                        self.taskName = self.employee.login_task_id[1];
                    }
                    if (self.employee.login_description) {
                        self.description = self.employee.login_description;
                    }
                }
            });
            var projectInfo = this._rpc({
                model: "project.project",
                method: "search_read",
                args: [[], ["id", "name"]]
            }).then(function (result) {
                self.projects = result;
            });

            return Promise.all([def, projectInfo, this._super.apply(this, arguments)
            ]);
        },

        OnChangeProject:  function(){
            console.log('Test1')
            var self = this;
            const project_id = this.$el.find('select#oe_project').find(":selected").val();
            var select_tareas = self.$el.find('select#oe_task')
            select_tareas.find("option").each(function() {
                $(this).remove();
            });
            this._rpc({
                model: "project.task",
                method: "search_read",
                args: [[["project_id", "=", parseInt(project_id)]], ["id", "name", "fold" ]]
            }).then(function(result) {
                self.tasks = result;
                self.tasks.forEach(function (task) {
                    if (!task.fold) {
                        select_tareas.append($('<option/>', {
                            value: task.id,
                            text: task.name,
                        }));
                    }
                });

            });

        },

        update_attendance: function () {
            const project_id = this.$el.find('select#oe_project').find(":selected").val();
            const task_id = this.$el.find('select#oe_task').find(":selected").val();
            var self = this;
            const description = this.$el.find('input#oe_description').val();
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                context: { project_id: project_id, task_id: task_id, description: description},
            })
            .then(function (result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.displayNotification({title: result.warning, type: 'danger'});
                }
            });
        },
    });

});