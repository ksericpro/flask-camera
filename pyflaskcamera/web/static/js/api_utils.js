var Api_Utils = {}

/* start generic promise api*/
Api_Utils.post = function(url, jsonlist, headers){
    var h = headers? headers:{ "Content-type": "application/json"};
    return new Promise(function(resolve, reject) {
      axios.post(url, jsonlist,
          {headers: h })
        .then(function (response) {
          resolve(response.data);
        })
        .catch(function (error) {
          if (error.response) {
            console.log(JSON.stringify(error.response.data.message));
            reject(error.response.data.message);
          } else {
            reject(error);
          }
        });
    });
}

Api_Utils.get = function(url, headers){
    var h = headers? headers:{ "Content-type": "application/json" };
  	return new Promise(function(resolve, reject) {
  		axios.get(url,
  				{headers: h })
  		  .then(function (response) {
  				resolve(response.data);
  		  })
  		  .catch(function (error) {
          if (error.response) {
            console.log(JSON.stringify(error.response.data.message));
            reject(error.response.data.message);
          } else {
            reject(error);
          }
  		  });
  	});
}

Api_Utils.delete = function(url, jsonlist, headers){
    var h = headers? headers:{ "Content-type": "application/json" };
    var d = jsonlist? jsonlist:{};
    return new Promise(function(resolve, reject) {
      axios.delete(url,
          { data:d, headers: h })
        .then(function (response) {
          resolve(response.data);
        })
        .catch(function (error) {
          if (error.response) {
            console.log(JSON.stringify(error.response.data.message));
            reject(error.response.data.message);
          } else {
            reject(error);
          }
        });
    });
}

Api_Utils.put = function(url, jsonlist, headers){
    var h = headers? headers:{ "Content-type": "application/json" };
  	return new Promise(function(resolve, reject) {
  		axios.put(url, jsonlist,
  				{headers: h })
  		  .then(function (response) {
  				resolve(response.data);
  		  })
  		  .catch(function (error) {
          if (error.response) {
            console.log(JSON.stringify(error.response.data.message));
            reject(error.response.data.message);
          } else {
            reject(error);
          }
  		  });
  	});
}
/* end generic promise api*/

Api_Utils.startvideo = function(id){
    var headers = { "Content-type": "application/json", "X-Api-Key":API_KEY }
    var jsonlist = JSON.stringify({"camera":id });
    return Api_Utils.post( "/bwc/api/start_camera", jsonlist, headers);
}

Api_Utils.stopvideo = function(){
    var headers = { "Content-type": "application/json", "X-Api-Key":API_KEY }
    return Api_Utils.get( "/bwc/api/stop_camera", headers);
}