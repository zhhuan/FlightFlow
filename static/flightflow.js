
window.onload = function(){
    var trackselect = document.querySelector(".search_in .trackSelect");
    var changeSearchStyle = function(){
        var optionvalue = trackselect.options[trackselect.selectedIndex].value;
        var elems = document.querySelectorAll("div[data-fa-search-type]");
        var i,elem;
        for( i = 0,len = elems.length;i < len; i++){
            elem = elems[i];
            if(elem.getAttribute("data-fa-search-type") == optionvalue){
                elem.classList.remove("hide");
                elem.classList.add("active");
            }
            else{
                elem.classList.remove("active");
                elem.classList.add("hide");
            }
        }

    };
    trackselect.addEventListener("change",changeSearchStyle,true);

    var width  = '100%';
    var height = 1000;

    var svg = d3.select("#home-right").append("svg")
        .attr("width", width)
        .attr("height", height);

    var projection = d3.geo.mercator()
                        .center([107, 31])
                        .scale(800)
                        .translate([600, 600]);

    var path = d3.geo.path().projection(projection);


    d3.json("../static/china.geojson", function(error, root) {

        if (error)
            return console.log(error);
        console.log(root.features);

        var map = svg.append("g")
        .attr("transform", "translate(0,0)");

        map.selectAll("path")
        .data( root.features )
        .enter()
        .append("path")
        .attr("stroke","#fff")
        .attr("stroke-width",1)
        .attr("fill", function(d,i){
            return "#F5F0E0";
        })
        .attr("d",path )
        .on("mouseover",function(d,i){
            d3.select(this)
            .attr("fill","#FD5858");
         })
        .on("mouseout",function(d,i){
             d3.select(this)
             .attr("fill","#F5F0E0");
        });

    });

    d3.json("../static/places.json",function (error,places) {

        var location = svg.selectAll(".location")
            .data(places.location)
            .enter()
            .append("g")
            .attr("class","location")
            .attr("transform",function (d) {
                //计算标注点位置
                var coor = projection([d.log,d.lat]);
                return "translate(" + coor[0]+","+coor[1]+")";
            });

        function mouseover() {
            var e = d3.event;
            var name = this.__data__.name;
            var flow = this.__data__.flow;
            var tooltip = document.createElement('div');
            tooltip.id = "tooltip";
            tooltip.style.top = e.pageY + "px";
            tooltip.style.left = e.pageX + "px";
            tooltip.style.position = "absolute";
            tooltip.innerHTML = '<span>'+name+'</span><span>'+flow+'</span>';
            document.body.appendChild(tooltip);

        }


        function mouseout() {
            var tooltip = document.querySelector("#tooltip");
            document.body.removeChild(tooltip);
        }

        //插入一个圆
        location.append("circle")
            .attr("r",function (d,i) {
                return d.flow;
            })
            .on("mouseover",mouseover)
            .on("mouseout",mouseout);

    });

    

};