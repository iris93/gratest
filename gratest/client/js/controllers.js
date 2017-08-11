angular.module('app.controllers', [])
//flag_search:搜索结果刷新
//flag2Load: 可以开始加载
// $rootScope.subgra= item.grade;年级
// $rootScope.sch=school.name;学院
// .constant('main_url','http://115.159.211.204:1688/')
.constant('main_url','http://127.0.0.1:1688/')
.controller('loginCtrl', function($scope,$state,$rootScope,$http,$ionicPopup,main_url,Storage,DATA) {
 
  $scope.go2school = function(username,password){
    $http({
        method  : 'POST',
        url     : main_url+'login/',
        data    : {username:username,password:password},
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    }).
    success( function (data) {
      if (data.mystatus === 'success') {
        Storage.set('mayI',{username:username,password:password});
        Storage.set('userschool',data.userschool)
        $rootScope.userschool=Storage.get('userschool')
        Storage.set('schools',data.schools)
        console.log(data.userschool)
        $rootScope.schools=Storage.get('schools')
        $state.go('schools',{},{location: 'replace'});
      }
      else {
        $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          // template:  'wrong name or password'
          template:  data.message,
        });
      }
    }).
    error(function (data) {
      $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          template:  '请求失败,请确认网络状态是否开通并稍后再试！'
      });
    })
  }
})

.controller('schoolsCtrl', function($scope,$cordovaGeolocation,$state,$http,$ionicPopup,$rootScope,$ionicLoading,Storage,DATA,main_url) {
    $scope.studenttypes = DATA.all_options_search();
    $rootScope.studenttype = $scope.studenttypes[0];
    $scope.go2searchs=function(){
    $state.go('search',{},{reload: true});
    }
  // $scope.schools = DATA.all_schools();
    $scope.schools=Storage.get('schools')
    $scope.back = function(){
      $state.go('tabhome.scores',{},{location: 'replace',reload: true});
    }

  $scope.toggleGrade = function(school) {
    school.subgrade = DATA.get_subgrade();
    school.show = !school.show;
  };
  $scope.changestutype = function(id){
    switch(id){
      case 0:$rootScope.studenttype = $scope.studenttypes[1];break;
      case 1:$rootScope.studenttype = $scope.studenttypes[0];break;
    }

  }
  $scope.isGradeShown = function(school) {
      return school.show;
  };
  
  $scope.go2scores = function(item,school){
    $state.go('tabhome.scores',{},{location: 'replace'});
    school.show = !school.show;
    $rootScope.subgra= item.grade;
    $rootScope.sch=school.name;
  } ;
    
})
    
.controller('tabhomeCtrl', function($scope,$state,$rootScope,$http,$ionicPopup,$ionicLoading,main_url,DATA) {
  $scope.change_schools=function(){
    $state.go('schools',{},{reload: true});
  }
  $scope.go2searchs=function(){
    $state.go('search',{},{reload: true});
  }
})

.controller('scoresCtrl', function($scope,$timeout,$http,$rootScope,$ionicPopup,$ionicLoading,DATA,main_url) {
  $scope.content="评分结果";
  $scope.toggle = function(student) {
  student.show = !student.show;
  }
  $scope.labels = ['专业技术类', '文学小说类', '趣味休闲类', '心理咨询类', '其他'];
  $scope.series = ['Series A'];
  $scope.data = [
    [18, 1, 0, 0, 3]
  ];
  $scope.isDetailShown=function(student){
    return student.show;
  }
  $scope.flag2Load = 0;
  //初始化信息加载---本地
  // $http.get("test/students.json")
  //   .success(function (response) {
  //     var flag=!flag;
  //     DATA.set_Results(response.students);
  //   // $scope.type = typeof (DATA.get_Results()[1].time)
  //   $rootScope.$watch('flag',function(){
  //   $scope.students=DATA.get_Results();
  //   });   
  //   }
  // );
  //初始化信息加载---下拉
  //这里测试加载数据
// $scope.doRefresh1 = function() {
//       $http.get("test/items.json").success(function (data) {
//       // $scope.items = data;
//       $ionicLoading.hide();
//       $ionicPopup.alert({
//           title: 'Message',
//           cssClass: 'alert-text',
//           template:  'success' });
//     var flag=!flag;
//     // DATA.set_Results(data.items);
//     DATA.add_Results(data.items1);
//     $rootScope.$watch('flag',function(){
//     $scope.items1=DATA.get_Results();
//     });
//       //console.log(data);
//     }).
//     error(function (data) {
//       $ionicPopup.alert({
//           title: 'Message',
//           cssClass: 'alert-text',
//           template:  'error' });
//     }).
//     finally(function() {
//       $scope.$broadcast('scroll.refreshComplete');
//       // refresh is over
//     });
//   };

  $scope.doRefresh = function(mystate1) {
    $scope.flag_number = 0;//初次查询，多多指教
    mystate1=mystate1||0;
    if (mystate1==1){}
     else{    
      $ionicLoading.show({
      content: '加载中',
      animation: 'fade-in',
      showBackdrop: true,
      maxWidth: 200,
      showDelay: 0,
      hideOnStateChange: false
    });}

    $http({
        method  : 'GET',
        url     : main_url+'stuinfo/',
        params    : {schoolname:$rootScope.sch,subgrade:$rootScope.subgra,studenttype:$rootScope.studenttype.show,number:$scope.flag_number},
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    }).success(function (data) {
      var flag=!flag;
      DATA.set_Results(data.students);
      $rootScope.$watch('flag',function(){
      $scope.students=DATA.get_Results();
        });
      $scope.flag2Load =1;
     
    }).
    error(function (data) {
      $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          template:  '请求失败,请确认网络状态是否开通并稍后再试' });
    }).
    finally(function() {
      $scope.$broadcast('scroll.refreshComplete');
      $scope.flag_number =  1;
       $ionicLoading.hide();
    });
  };
  $scope.loadData = function() {
    $scope.flag_number = 0;//初次查询，多多指教
      $ionicLoading.show({
      content: '加载中',
      animation: 'fade-in',
      showBackdrop: true,
      maxWidth: 200,
      showDelay: 0,
      hideOnStateChange: false
    });

    $http({
        method  : 'GET',
        url     : main_url+'stuinfo/',
        params    : {schoolname:$rootScope.sch,subgrade:$rootScope.subgra,studenttype:$rootScope.studenttype.show,number:$scope.flag_number},
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    }).success(function (data) {
     var flag=!flag;
      DATA.set_Results(data.students);
      $rootScope.$watch('flag',function(){
      $scope.students=DATA.get_Results();
        });
      $scope.flag2Load =1;
    }).
    error(function (data) {
      $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          template:  '请求失败,请确认网络状态是否开通并稍后再试' });
    }).
    finally(function() {
      $scope.$broadcast('scroll.refreshComplete');
      $scope.flag_number =  1;
       $ionicLoading.hide();
    });
  };
  $rootScope.$watch('subgra', $scope.loadData)
  $rootScope.$watch('flag_search', function(){
    $scope.students=DATA.get_Results();
  });

  //上划加载数据
  $scope.ready2Load = function(){
    if ($scope.students.length>10) 
      {return $scope.flag2Load}
  };
  $scope.loadMoreData = function() {
    $ionicLoading.show({
      content: '加载中',
      animation: 'fade-in',
      showBackdrop: true,
      maxWidth: 200,
      showDelay: 0,
      hideOnStateChange: false
    });
    $http({
        method  : 'GET',
        url     : main_url+'stuinfo/',
        params    : {schoolname:$rootScope.sch,subgrade:$rootScope.subgra,studenttype:$rootScope.studenttype.show,number:$scope.flag_number},
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    }).
    success(function (data) {
      // $scope.items = data;
      //console.log(data);
      
      DATA.add_Results(data.students);
       if (data.length<1) {$scope.flag2Load=0;}
       else{
        $scope.flag2Load=1;
         var flag=!flag;
       }
      $ionicLoading.hide();
      $rootScope.$watch('flag',function(){
          $scope.students=DATA.get_Results();
        }); 
    }).
    error(function (data) {
      $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          template:  '请求失败,请确认网络状态是否开通并稍后再试' })
    }).
    finally(function() {
      $scope.$broadcast('scroll.infiniteScrollComplete');
      $scope.flag_number +=1
    });
  };


})

.controller('settingCtrl', function($scope,$ionicPopup,$state,Storage,$rootScope,$http,main_url) {
  // $scope.userimg = "/resource/default.png";
  $scope.userimg = '/resource/tj_logo.jpg';
  $scope.changeimg = function (argument) {
  };
  $scope.$on('$ionicView.beforeEnter', function() {  
  console.log('beforeEnter'); 
    $rootScope.username = Storage.get('mayI').username;
    $rootScope.password = Storage.get('mayI').password;
    $scope.userschool = Storage.get('userschool');
    $scope.feedForm.feedbackcontent='';
});   


  $scope.logout = function(){
   var confirmPopup = $ionicPopup.confirm({
     title: Storage.get('mayI').username,
     template: '确定要注销登录码?'
   });
   confirmPopup.then(function(res) {
     if(res) {
       Storage.remove("mayI");
       Storage.remove("userschool");
       $state.go('login',{},{location: 'replace'});
     } else {
     };
   });
   };

   $scope.queryMode ={feedbackcontent:''};
   $scope.queryMode.feedbackcontent = '';
   $scope.feedback = function (feedbackcontent) {
             if (feedbackcontent.length<10) {
               $ionicPopup.alert({
                        title: '消息',
                        cssClass: 'alert-text',
                        template:  '问题描述不能少于10个字符！'
                      });
             }else{
              $scope.queryMode.feedbackcontent = '';
              $state.go('options.morePage',{},{location: 'replace',reload: true});
              $http({
                method  : 'POST',
                url     : main_url+'feedback/',
                data    : {content:feedbackcontent},
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
                }
            }).success( function (data) {    
                 $ionicPopup.alert({
                        title: '消息',
                        cssClass: 'alert-text',
                        template:  '提交成功，谢谢反馈！'
                      });
            }).error(function (data) {
              $ionicPopup.alert({
                  title: '消息',
                  cssClass: 'alert-text',
                  template:  '提交成功，谢谢反馈！'
              });
            })
           }         
    }
})

.controller('searchCtrl', function($scope,$state,$rootScope,$http,$ionicPopup,$ionicLoading,DATA,main_url) {
  $scope.back = function(){
      $state.go('tabhome.scores',{},{location: 'replace',reload: true});
  }
  $scope.search = function(student_id){
    $ionicLoading.show({
      content: '加载中',
      animation: 'fade-in',
      showBackdrop: true,
      maxWidth: 200,
      showDelay: 0,
      hideOnStateChange: false
    });
    $http({
        method  : 'GET',
        url     : main_url+'search/',
        params    : {student_id:student_id},
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    }).
    success(function (data) {
      if(data.students.length == 0)
        $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          template:  "对不起，未查找到结果" });
      else{
        DATA.set_Results(data.students);
        $rootScope.flag_search = !$rootScope.flag_search;
      };
      $ionicLoading.hide();
    }).
    error(function (data) {
      $ionicLoading.hide();
      $ionicPopup.alert({
          title: '消息',
          cssClass: 'alert-text',
          template:  '请求失败,请确认网络状态是否开通并稍后再试' });
    });
      $state.go('tabhome.scores',{},{location: 'replace'});
  }
})
