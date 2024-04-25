odoo.define('hr_attendance_apexive.my_attendances', function (require) {
    "use strict";

    var MyAttendances = require('hr_attendance.my_attendances');
    var field_utils = require('web.field_utils');

    const session = require('web.session');
    MyAttendances.include({

        //this Owl event allows the MyAttendances component to handle
        // the change event of the oe_project element by invoking
        // the OnChangeProject method when the element's value changes.

        events: _.extend({}, MyAttendances.prototype.events, {
            'change #oe_project': 'OnChangeProject',
        }),


        // willStart function fetches data about the current user's attendance and available projects from the server,
        // processes the retrieved data, and ensures that the component starts rendering only after all required
        // data is available.

        willStart: function () {
            var self = this;
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

            // This line returns a Promise that resolves when all asynchronous operations (RPC calls) are complete.

            return Promise.all([def, projectInfo, this._super.apply(this, arguments)
            ]);
        },


        //OnChangeProject function updates the tasks dropdown based on the selected project,
        // ensuring that only relevant tasks are displayed for the selected project.

        OnChangeProject:  function(){
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

        //this update_attendance function updates the attendance record of the current employee with the selected
        // project, task, and description and handles the response from the server accordingly,
        // either by executing an action or displaying a warning notification.

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