(function () {
    var allGde = ["Leaderboard#1", "Badge#1", "Leaderboard#2", "Badge#2"];

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
        createGDEPath: "",
        selfInstances: [],
        getSelfInstances: function() {
            return this.get('selfInstances');
        }.property(),
        gdeTypeInitialize: function() {
            var arr = [];
            arr.push(GDE.create({
                'name': 'Leader Board',
                'path': 'leaderboard'
            }));
            arr.push(GDE.create({
                'name': 'Badge',
                'path': 'badge'
            }));
            arr.push(GDE.create({
                'name': 'Avatar',
                'path': 'avatar'
            }));
            this.set('gdeType', arr);
        }.on('init'),
        selfInstancesInitialize: function() {
            var arr = [];
            arr.push(Instance.create({
                'name': 'Leaderboard#1'
            }));
            arr.push(Instance.create({
                'name': 'Badge#1'
            }));
            arr.push(Instance.create({
                'name': 'Leaderboard#2'
            }));
            arr.push(Instance.create({
                'name': 'Badge#2'
            }));
            this.set('selfInstances', arr);
        }.on('init'),
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
            createGDESelect: function(val) {
                this.set('createGDEPath', val);
            },
            createNewGDE: function() {
                var arr = this.get('selfInstances');
                var name = this.get('createGDEName');
                //arr.push(Instance.create({
                //    'name': name
                //}));
                arr.push(arr[1]);
                this.set('selfInstances', arr);
                console.log(this.get('createGDEName'));
                console.log(arr);
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