(function () {
    var cAjax = function (obj) {
        return $.ajax({
            dataType: obj['dataType'] ? obj['dataType'] : "JSON",
            url: obj['url'],
            type: obj['type'] ? obj['type'] : "GET",
            data: obj['data'],
            retryCount: obj['retryCount'] ? obj['retryCount'] : 0,
            retryLimit: 10,
            success: function (data) {
                if (typeof obj['success'] == 'function') {
                    obj['success'](data);
                }
            },
            error: function (data) {
                if (data.status > 498 && this.retryCount < this.retryLimit) {
                    obj['retryCount'] = obj['retryCount'] ? obj['retryCount'] + 1 : 1;
                    setTimeout(function () {
                        cAjax(obj);
                    }, 2000);
                } else {
                    if (typeof obj['error'] == 'function') {
                        obj['error'](data);
                    }
                }
            }

        });
    };

    App = Ember.Application.create({
        rootElement: '#everything'
    });

    App.ApplicationController=Ember.Controller.extend({
        isLogin: false,
        isFormSubmit: false,
        lowerMessage: "",
        show_success: false,
        show_error: false,
        api_response: [],
        backEndURL: "/backend",
        signInEndpoint: "/sign",
        registerEndpoint: "/register",
        checkEndpoint: "/check",
        getURL: function(endpoint) {
            return this.get('backEndURL') + this.get(endpoint);
        },
        checkIfLoggedIn: function() {
            var parent = this;
            var success = function(data) {
                if(data.success) {
                    document.location.href = "/";
                }
            };
            cAjax({
                type: 'GET',
                url: parent.getURL('checkEndpoint'),
                success: success
            });
        }.on('init'),
        clearForm: function() {
            if(this.get('show_success')) {
                this.set('fullName', '');
                this.set('email', '');
                this.set('password', '');
            }
        }.observes('show_success'),
        makeSignInRequest: function() {
            var parent = this;
            var success = function(data) {
                if(data.success) {
                    document.location.href = "/";
                } else {
                    parent.set('show_error', true);
                }
                parent.set('api_response', data.message);
                parent.toggleProperty('isFormSubmit');
            };
            cAjax({
                type: 'POST',
                url: parent.getURL('signInEndpoint'),
                data: {
                    'email': parent.get('email'),
                    'password': parent.get('password')
                },
                success: success
            });
        },
        makeRegisterRequest: function() {
            var parent = this;
            var success = function(data) {
                if(data.success) {
                    parent.set('show_success', true);
                } else {
                    parent.set('show_error', true);
                }
                parent.set('api_response', data.message);
                parent.toggleProperty('isFormSubmit');
            };
            cAjax({
                type: 'POST',
                url: parent.getURL('registerEndpoint'),
                data: {
                    'fullname': parent.get('fullName'),
                    'email': parent.get('email'),
                    'password': parent.get('password')
                },
                success: success
            });
        },
        clearMessages: function() {
            this.set('show_success', false);
            this.set('show_error', false);
        },
        actions: {
            toggleLogin: function () {
                this.toggleProperty('isLogin');
            },
            register: function() {
                if(!this.get('isFormSubmit')) {
                    this.toggleProperty('isFormSubmit');
                    this.clearMessages();
                    this.makeRegisterRequest();
                    this.set('request_type', 'register');
                }
                else {
                    this.set('lowerMessage', 'Please wait... :(')
                }
            },
            signIn: function() {
                if(!this.get('isFormSubmit')) {
                    this.toggleProperty('isFormSubmit');
                    this.clearMessages();
                    this.makeSignInRequest();
                    this.set('request_type', 'sign');
                }
                else {
                    this.set('lowerMessage', 'Please wait... :(')
                }
            }
        }
    });

})();