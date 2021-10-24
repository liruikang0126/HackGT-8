load();

function load() {
  $.ajax({
    url: '/getData/',
    type: 'POST',
    data: 'data request',
    dataType: 'json',
    success: function (data) {
      showData(data);
    }
  })
}



function showData(result) {
  //console.log(result);
  var data = result['data'];

  data.sort(function (a, b) {
    return a.x.localeCompare(b.x);
  });

  var container = d3.select("#list");
  var group = container.append('g');
  const alph = ['0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z'];
  var curr = 0;
  data.forEach(function (element) {
    var newAlph = false;
    while (element.x[0] != alph[curr]) {
      curr = curr + 1;
      newAlph = true;
    }
    if (newAlph == true) {
      group.append('div')
        .text(element.x[0])
        .attr('class', 'alphNote')
    }
    group.append('div')
      .text(function (e) {
        var str = [];
        str.push(
          element.x,
          "  (",
          element.time,
          "min)"
        );
        return str.join("");
      })
      .attr('id', element.id)
      .attr('class', 'listItem')
      .on("mouseover", handleMouseOver)
      .on("mouseout", handleMouseOut);
  })




  /*data.forEach(function(element) {
  //console.log(element)
      group.append('div')
        .text(element.x)
        .attr('id', element.id)
        .attr('class', 'listItem')
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);
  });*/

  function handleMouseOver() {  // Add interactivity

    d3.select(this).style('color', '#f44336');
    var thisID = this.id;
    drawCloudFocused(thisID);

  }

  function handleMouseOut() {

    d3.select(this).style('color', '#9e9e9e');
    document.getElementById("cloud").remove();
    drawCloudDefault();
  }

  function drawCloudDefault() {
    d3.select("#container")
      .append('div')
      .attr('id', 'cloud')
      .style('height', '100%')
      .style('width', '100%');
    var chart = anychart.tagCloud(data);


    chart.container("cloud");
    chart.angles([0]);
    chart.tooltip().format("Estimated Waiting Time: {%time} min\n\n");
    /*chart.listen("pointsHover", function(e){
      var thisID = e.point.get("id");
      drawCloudFocused(thisID);
    });
    chart.listen("pointMouseOut", function(e){
      drawCloudDefault();
    });*/
    chart.draw();
  }

  function drawCloudFocused(thisID) {
    data.forEach(function (element) {
      if (element.id == thisID) {
        element['category'] = true.toString();

      }
      else {
        element['category'] = false.toString();
      }
      //console.log(element);
    });
    //console.log(data);

    // set the container id
    document.getElementById("cloud").remove();

    d3.select("#container")
      .append('div')
      .attr('id', "cloud")
      .style('height', '100%')
      .style('width', '100%');
    chart = anychart.tagCloud(data);
    chart.container("cloud");
    var customColorScale = anychart.scales.ordinalColor();
    customColorScale.colors(["#9e9e9e", "#f44336"]);
    chart.colorScale(customColorScale);
    chart.angles([0]);
    data.forEach(function (element) {
      delete element.category;
    })

    chart.draw();


    //console.log(data);
  }

  drawCloudDefault();

  var merchant = d3.select('#merchants')
  //console.log()
  data.forEach(function (element) {
    //console.log(element.x)
    merchant.append('option')
      .attr('value', element.x)
      .text(element.x)
  })

  upload(data);
  displayIntro();


}




function upload(data) {
  $('#lgbut_compute').click(function () {

    formdata = new FormData();
    var file = $("#file")[0].files[0];
    formdata.append("image", file);
    var selection = document.getElementById("merchants");
    var id = 0;
    data.forEach(function (element) {
      if (selection.value == element.x) {
        console.log(element.x);
        id = element.id;

      }
    })
    formdata.append("id", id)
    console.log(formdata)
    $.ajax({
      url: '/recognition/',
      type: 'POST',
      data: formdata,
      dataType: 'json',
      processData: false,
      contentType: false,
      success: window.location.reload(false)
    })
  })

  function ProcessFile(e) {
    var file = document.getElementById('file').files[0];
    if (file) {
      var reader = new FileReader();
      reader.onload = function (event) {
        var txt = event.target.result;

        var img = document.createElement("img");
        img.src = txt;
        document.getElementById("result").appendChild(img);
      };
    }
    reader.readAsDataURL(file);
  }
  function contentLoaded() {
    document.getElementById('file').addEventListener('change',
      ProcessFile, false);
  }
  window.addEventListener("DOMContentLoaded", contentLoaded, false);
}

function displayIntro() {

  $('#userguide').click(function () {
    console.log('test');
    introJs().setOptions({
      nextLabel: 'next $rarr;',
      prevLabel: '$larr; previous',
      skipLabel: 'exit',
      doneLabel: 'done'
    }).start();
  });

}