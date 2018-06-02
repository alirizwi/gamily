(function () {
    var allGde = ["Leaderboard#1", "Badge#1", "Leaderboard#2"];

    var cAjax = function (obj) {
        return $.ajax({
            dataType: obj['dataType'] ? obj['dataType'] : "JSON",
            url: obj['url'],
            type: obj['type'] ? obj['type'] : "GET",
            data: obj['data'],
            retryCount: obj['retryCount'] ? obj['retryCount'] : 0,
            retryLimit: 2,
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
                    }, 1000);
                } else {
                    if (typeof obj['error'] == 'function') {
                        obj['error'](data);
                    }
                }
            }

        });
    };

    var GDE = Ember.Object.extend({
        name: "GDE Name",
        path: "gde_url_prefix"
    });

    var Instance = Ember.Object.extend({
        name: "Instance"
    });

    var Rule = Ember.Object.extend({
        name: "Rule Name",
        action: "take",
        meaning: "Decrease points of users",
        value: 20,
        enabled: true,
        event: "comment_posted",
        gde: function() {
            items = allGde;
            return items[Math.floor(Math.random()*items.length)]
        }.property()
    });

    App = Ember.Application.create({
        rootElement: '#dashboard-app'
    });

    App.ApplicationController=Ember.Controller.extend({
        fullName: "LoggedIn User",
        email: 'admin@gamily.in',
        gdeType: [],
        api_response: 0,
        ajaxResponse: '',
        ajaxURL: '',
        badgesURL: '/backend/badges/list',
        leaderboardURL: '/backend/leaderboard/list',
        gdeURL: 'backend/gde/list',
        gdeResponse: '',
        createGDEPath: "",
        getData: "{}",
        selfInstances: [],
        getSelfInstances: function() {
            return this.get('selfInstances');
        }.property('selfInstances'),
        gdeTypeInitialize: function() {
            var parent = this;
            var success = function(data) {
                parent.set('gdeResponse', data);
            };
            cAjax({
                type: 'GET',
                url: parent.gdeURL,
                data: JSON.parse(this.get('getData')),
                success: success
            });
        }.on('init'),
        fetchData: function(url) {
            var parent = this;
            var success = function(data) {
                parent.set('ajaxResponse', data);
            };
            cAjax({
                type: 'GET',
                // url: this.get('ajaxURL'),
                url: url,
                data: JSON.parse(this.get('getData')),
                success: success
            });
        }.observes('ajaxURL'),
        selfInstancesInitialize: function() {
            var parent = this;
            var arr = [];

            parent.fetchData(this.leaderboardURL);
            parent.fetchData(this.badgesURL);

        }.on('init'),
        processData: function() {
            response = this.get('ajaxResponse');
            console.log('finally')
            console.log(response);
            if(response != '') {
                console.log("response is: " + response);
                console.log(response.data);
                // this.getResponse();
                this.gdeInitialize();

            }
        }.observes('ajaxResponse'),
        gdeInitialize: function() {
            var arr = [];
            console.log(this.get('ajaxURL'));
            instances = this.get('selfInstances');
            for(var i=0;i<instances.length;i++) {
                arr.push(instances[i]);
            }
            response = this.get('ajaxResponse');
            for(var i=0;i<response.data.length; i++) {
                name = response.data[i].name;
                arr.push(Instance.create({
                    'name': name
                }));
            }

            this.set('selfInstances', arr);
            // console.log(this.get('selfInstances'));
        },
        processGDE: function() {
            var arr=[];
            response = this.get('gdeResponse');
            for(var i=0;i<response.data.length; i++) {
                name = response.data[i].name;
                path = response.data[i].path;
                arr.push(GDE.create({
                    'name': name,
                    'path': path
                }));
            }
            this.set('gdeType', arr);
        }.observes('gdeResponse'),
        createGDERequest: function() {
            var parent = this;
            var success = function(data) {
                if(data.success) {
                    // parent.set('show_success', true);
                    alert(data.message);
                    console.log(data.message);
                    document.location.href = "/";
                } else {
                    // parent.set('show_error', true);
                }

            };
            path = this.get('createGDEPath');
            console.log(this.get('createGDEName'));
            console.log(this.get('createGDEDescription'));
            console.log(this.get('createBadgeImageName'));
            if(path == 'badge'){
                cAjax({
                    type: 'POST',
                    url: 'backend/' + this.get('createGDEPath') + 's/create',
                    data: {
                        'name': parent.get('createGDEName'),
                        'description': parent.get('createGDEDescription'),
                        'image_name': parent.get('createBadgeImageName')
                    },
                    success: success
                });
            }
            else {
                cAjax({
                    type: 'POST',
                    url: 'backend/' + this.get('createGDEPath') + '/create',
                    data: {
                        'name': parent.get('createGDEName'),
                        'description': parent.get('createGDEDescription'),
                    },
                    success: success
                });
            }

        },
        loadingLeaf: true,
        profilePicture: function () {
            return 'http://www.gravatar.com/avatar/' + CryptoJS.MD5(this.get('email'));
        }.property('email'),
        allRuless: function() {
            var arr = [];
            for(var i=0; i<10; i++) {
                var rule = Rule.create();
                arr.push(rule);
            }
            this.set('allRules', arr);
            return arr;
        }.on('init'),
        allRules: [],
        currentGDE: "Leaderboard#1",
        allGde: allGde,
        createGDEOn: false,
        currentBadge: false,
        currentRules: function() {
            allRules = this.get('allRules');
            currentRulesList = [];
            currentGDE = this.get('currentGDE');
            for(var i=0; i<allRules.length; i++) {
                if(allRules[i].get('gde') === currentGDE) {
                    currentRulesList.push(allRules[i]);
                }
            }
            return currentRulesList;
        }.observes('currentGDE','allRules').property('currentGDE','allRules'),
        actions: {
            toogleEnabled: function(context) {
                context.set('enabled', !(context.get('enabled')));
            },
            changeCurrentGDE: function (new_current) {
                this.set('currentGDE', new_current);
            },
            signout: function() {
                var parent = this;
                var success = function(data) {
                    if(data.success) {
                        parent.cleanPrivateData();
                        document.location.href = "/auth";
                    }
                };
                cAjax({
                    type: 'GET',
                    url: parent.getURL('signOutEndpoint'),
                    success: success
                });
            },
            newGDEToggle: function() {
                this.toggleProperty('createGDEOn');
            },
            badgeImageToggle: function() {
                this.toggleProperty('currentBadge');
            },
            createGDESelect: function(val) {
                console.log("Here it is;");
                this.set('createGDEPath', val);
                console.log(this.get('createGDEPath'));
                if(this.get('createGDEPath')=='badge'){
                    this.set('currentBadge',true);
                    console.log("yo");
                }
                else {
                    this.set('currentBadge',false);
                }
                
            },
            createNewGDE: function() {

                var arr = this.get('selfInstances');
                var name = this.get('createGDEName');
                var description = this.get('createGDEDescription');
                arr.push(Instance.create({
                   'name': name
                }));
                // arr.push(arr[1]);
                this.set('selfInstances', arr);
                console.log(this.get('createGDEPath'));
                console.log(this.get('createGDEName'));
                console.log(this.get('createGDEDescription'));
                console.log(arr);
                this.createGDERequest();
            }
        },
        backEndURL: "/backend",
        checkEndpoint: "/check",
        signOutEndpoint: "/logout",
        getURL: function(endpoint) {
            return this.get('backEndURL') + this.get(endpoint);
        },
        checkIfLoggedIn: function() {
            var parent = this;
            var success = function(data) {
                if(!data.success) {
                    document.location.href = "/auth";
                } else {
                    parent.set('fullName', data.user.fullname);
                    parent.set('email', data.user.email);
                    parent.set('loadingLeaf', false);
                }
            };
            var error = function(data) {
                document.location.href = "/auth";
            };
            cAjax({
                type: 'GET',
                url: parent.getURL('checkEndpoint'),
                success: success,
                error: error,
                retryLimit: 2
            });
        }.on('init'),
        cleanPrivateData: function() {
            this.set('fullName', 'LoggedIn User');
            this.set('email', 'admin@gamily.in')
        }
    });

})();