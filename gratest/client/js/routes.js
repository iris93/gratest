angular.module('app.routes', [])

.config(function($stateProvider, $urlRouterProvider,$ionicConfigProvider) {

         $ionicConfigProvider.platform.ios.tabs.style('standard'); 
         $ionicConfigProvider.platform.ios.tabs.position('bottom');
         $ionicConfigProvider.platform.android.tabs.style('standard');
         $ionicConfigProvider.platform.android.tabs.position('bottom');

        $ionicConfigProvider.platform.ios.navBar.alignTitle('center'); 
        $ionicConfigProvider.platform.android.navBar.alignTitle('center');

        $ionicConfigProvider.platform.ios.backButton.previousTitleText('').icon('ion-ios-arrow-thin-left');
        $ionicConfigProvider.platform.android.backButton.previousTitleText('').icon('ion-android-arrow-back');        

        $ionicConfigProvider.platform.ios.views.transition('ios'); 
        $ionicConfigProvider.platform.android.views.transition('android');
  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider

    .state('login', {
      url: '/page1',
      cache: 'false',
      templateUrl: 'templates/login.html',
      controller: 'loginCtrl'
    })
        
         
    .state('schools', {
      url: '/page2',
      cache: 'false',
      templateUrl: 'templates/schools.html',
      controller: 'schoolsCtrl'
    })
        
    .state('tabhome', {
      url: '/page3',
      abstract:true,
      templateUrl: 'templates/tabhome.html',
      controller: 'tabhomeCtrl'
    })

    .state('tabhome.scores', {
      url: '/page3_1',
      views: {
        'tab1': {
          templateUrl: 'templates/scores.html',
          controller: 'scoresCtrl'
        }
      }
    })
  
    .state('tabhome.setting', {
      url: '/page3_2',
      views: {
        'tab2': {
          templateUrl: 'templates/setting.html',
          controller: 'settingCtrl'
        }
      }
    })


    .state('search', {
      url: '/page4',
      cache: 'false',
      templateUrl: 'templates/search.html',
      controller: 'searchCtrl'
    })
    
    $urlRouterProvider.otherwise('/page1');

});