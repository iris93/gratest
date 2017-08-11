// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
angular.module('app', ['ionic', 'app.controllers', 'app.routes', 'app.services','chart.js','ngCordova'])

.run(function($ionicPlatform,$ionicHistory,$location,$cordovaToast,$rootScope,$timeout,$state,$http,Storage,main_url) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if(window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if(window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });

  $ionicPlatform.registerBackButtonAction(function (e) {  
      //判断处于哪个页面时双击退出  
      if ($location.path() == '/page3/page3_1' || $location.path() == '/page3/page3_2' ||$location.path() == '/page3/page3_3' || $location.path() == '/page1') {  
          if ($rootScope.backButtonPressedOnceToExit||$rootScope.exitflag) {  
              ionic.Platform.exitApp();  
          }
          else {  
              $rootScope.backButtonPressedOnceToExit = true;  
              $cordovaToast.showShortBottom('再按一次退出');  
              setTimeout(function () {  
                  $rootScope.backButtonPressedOnceToExit = false;  
              }, 2000);  
          }  
      }  
      else if ($ionicHistory.backView()) {  
          $ionicHistory.goBack();  
      } else {  
          $rootScope.backButtonPressedOnceToExit = true;  
          $cordovaToast.showShortBottom('再按一次退出');  
          setTimeout(function () {  
              $rootScope.backButtonPressedOnceToExit = false;  
          }, 2000);  
      }  
      e.preventDefault();  
      return false;  
  }, 101);


  if(Storage.get('mayI')){
    $location.path('/page2');
    $http({
        method  : 'POST',
        url     : main_url+'login/',
        data    : Storage.get('mayI'),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    }).
    success(function (data){
      $rootScope.usertype=Storage.get('usertype')
    }).
    error(function (data) {
      console.log(data);
    });
  } 
  else {
    console.log("login error");
    // $scope.already = true;
  }
})