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
        name: "Instance",
        numRules: 0
    });

    var Rule = Ember.Object.extend({
        name: "Rule Name",
        action: "take",
        meaning: "Decrease points of users",
        value: "20",
        // enabled: true,
        event: "comment_posted",
        gdeid: "1",
        gdetype: "leaderboard",
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
        currentRuleAction: "",
        currentRuleEvent: "",
        getData: "{}",
        selfInstances: [],
        isSuccess: false,
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
                url: url,
                data: JSON.parse(this.get('getData')),
                success: success
            });
        },
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
            console.log("URL:"+this.get('ajaxURL'));
            instances = this.get('selfInstances');
            for(var i=0;i<instances.length;i++) {
                arr.push(instances[i]);
            }
            resp = this.get('ajaxResponse');
            for(var i=0;i<response.data.length; i++) {
                name = response.data[i].name;
                id = response.data[i].id;
                type = response.data[i].type;
                arr.push(Instance.create({
                    'name': name,
                    'id': id,
                    'type': type
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
                    // document.location.href = "/";
                    location.reload(true);
                } else {
                    this.toggleProperty('isSuccess');
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
        isSuccessToggle: function() {
            this.toggleProperty('isSuccess');
        }, 
        createRuleRequest: function(){
            var parent = this;
            var success = function(data) {
                if(data.success) {
                    // parent.set('show_success', true);
                    alert(data.message);
                    // this.isSuccessToggle();
                    console.log(data.message);
                    location.reload(true);
                    // console.log(this.get('GDEOn'));
                    parent.changeCurrentGDE(parent.get('GDEOn'));
                } else {
                    // parent.set('show_error', true);
                    // console.log(this.get('GDEOn'));
                    console.log("nhi hua");
                }

            };

            cAjax({
                type: 'POST',
                url: 'backend/' + 'rules/create',
                data: {
                    'name': this.get('createRuleName'),
                    'event': this.get('currentRuleEvent'),
                    'action': this.get('currentRuleAction'),
                    'meaning': this.get('createRuleMeaning'),
                    'value': this.get('createRuleValue'),
                    'gde_id': this.get('GDEid'),
                    'gde_type': this.get('GDEtype'),
                },
                success: success
            });
            console.log('name:', this.get('createRuleName'));
            console.log('event:', this.get('currentRuleEvent'));
            console.log('action:', this.get('currentRuleAction'));
            console.log('meaning:', this.get('createRuleMeaning'));
            console.log('value:', this.get('createRuleValue'));
            console.log('gde_id:', this.get('GDEid'));
            console.log('gde_type:', this.get('GDEtype'));
        },
        loadingLeaf: true,
        profilePicture: function () {
            return 'http://www.gravatar.com/avatar/' + CryptoJS.MD5(this.get('email'));
        }.property('email'),
        allRuless: function(id, type) {
            var arr = [];
            // for(var i=0; i<10; i++) {
            //     var rule = Rule.create();
            //     arr.push(rule);
            // }
            // this.set('allRules', arr);
            var parent = this;
            console.log("id here"+this.get('GDEid'));
            var success = function(data) {
                parent.set('allRules', data);
                console.log("RUles:" + allRules);
            };
            cAjax({
                type: 'GET',
                url: '/backend/rules/list',
                data: {
                    'id': id,
                    'type': type
                },
                success: success
            });
            return arr;
        },
        allRules: [],
        allActions: [],
        allEvents: [],
        currentGDE: "",
        allGde: allGde,
        GDEOn: "",
        GDEid: 0,
        GDEtype: "",
        numberOfRules: 0,
        createGDEOn: false,
        createRuleOn: false,
        currentBadge: false,
        currentRules: function() {
            allRules = this.get('allRules');
            currentRulesList = [];
            currentGDE = this.get('currentGDE');
            if(allRules!='')
                this.rulesInitialise();
            console.log("allRules: " + allRules);
            return currentRulesList;
        }.observes('allRules').property('allRules'),    
        
        // }.observes('currentGDE','allRules').property('currentGDE','allRules'),
        rulesInitialise: function() {
            allRules = this.get('allRules');
            currentRulesList = [];
            currentGDE = this.get('currentGDE');
            for(var i=0; i<allRules.data.length; i++) {
                // if(allRules[i].get('gde') === currentGDE) {
                    currentRulesList.push(allRules.data[i]);
                    console.log("yay:"+allRules.data[i].action);
                // }
            }
        },
        fetchActions: function(path) {
            var parent = this;
            // console.log("id here"+this.get('GDEid'));
            // var path=this.get('GDEtype');
            var success = function(data) {
                parent.set('allActions', data);
                // console.log("actions:" + parent.get('allActions'));
            };
            if(path=='badge')
                path='badges';
            cAjax({
                type: 'GET',
                url: '/backend/'+path+'/actions',
                data: {},
                success: success
            });
        },
        fetchEvents: function() {
            var parent = this;
            var success = function(data) {
                parent.set('allEvents', data);
                console.log("Events in");
                console.log(parent.get('allEvents'))
                // console.log("RUles:" + allActions);
            };
            cAjax({
                type: 'GET',
                url: '/backend/events/list',
                data: {},
                success: success
            });
        },
        currentEvents: function() {
            allEvents = this.get('allEvents');
            currentEventsList = [];
            if(allEvents!=''){
                for(var i=0; i<allEvents.data.length; i++) {
                    // if(allRules[i].get('gde') === currentGDE) {
                        currentEventsList.push(allEvents.data[i]);
                        console.log("EEE:"+allEvents.data[i].name);
                    // }
                }
            }
            console.log("allEvents: " + allEvents);
            return currentRulesList;
        }.observes('allEvents').property('allEvents'),   


        actions: {
            toogleEnabled: function(context) {
                context.set('enabled', !(context.get('enabled')));
            },
            changeCurrentGDE: function (new_current) {
                this.set('GDEOn', new_current);
                console.log(this.get('GDEOn'));
                this.set('currentGDE', new_current.name);
                this.set('GDEid', new_current.id);
                this.set('GDEtype', new_current.type);
                this.allRuless(new_current.id, new_current.type);
                this.set('createRuleOn',false);
                this.fetchActions(new_current.type);
                this.fetchEvents();
                // this.getActions(new_current.type);
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
            newRuleToggle: function() {
                this.toggleProperty('createRuleOn');
                // this.getActions();
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
            createRuleAction: function(val) {
                console.log("Here it is;");
                this.set('currentRuleAction', val);
                console.log(this.get('currentRuleAction'));
               
            },
            createRuleEvent: function(val) {
                console.log("it is;");
                this.set('currentRuleEvent', val);
                console.log(this.get('currentRuleEvent'));
               
            },
            createNewGDE: function() {

                var arr = this.get('selfInstances');
                var name = this.get('createGDEName');
                var description = this.get('createGDEDescription');
                console.log(arr);
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
            },
            createNewRule: function() {
                console.log(this.get('createRuleName'));
                console.log(this.get('createRuleName'));
                // console.log(arr);
                this.createRuleRequest();
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