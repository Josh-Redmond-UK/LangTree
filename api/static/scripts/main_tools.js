
window.onload = init;

function init(){

let user_text = ""

let socket;

async function get_tree(text) {
    const k = document.getElementById('k-input').value;
    const depth = document.getElementById('depth-input').value;
    user_text = text;

    //var main_ui = document.getElementById('main-ui');
    //main_ui.innerHTML = '<div style="bottom:50%; width:50%; text-align: center; margin:auto"> <h1>Loading...</h1> </div>';

    // Close existing socket if it exists
    if (socket) {
        socket.close();
    }

    // Create a new WebSocket connection
    socket = new WebSocket(`wss:hammerhead-app-82aq3.ondigitalocean.app/langtree-api2/ws/tree/`);

    socket.onopen = function(e) {
        console.log("WebSocket connection established");
        WebSocket.send(`?text=${encodeURIComponent(text)}&k=${k}&max_depth=${depth}`)
        socket.addEventListener("message", (event) => {console.log("received message using listener")})
        const input_section = document.getElementById('text-container');
        input_section.style.display = 'none';
        const footer = document.getElementById('page_footer');
        footer.style.display = 'none';
        const drawer = document.getElementById('drawer_container');
        drawer.style.display = 'none';


    };


  socket.onmessage = function(event) {
    console.log("received message")
      const message = JSON.parse(event.data);
      if (message.type === "node") {
          updateTree(message.data);
      } else if (message.type === "complete") {
          console.log("Tree generation complete");
      }
  };

    socket.onerror = function(error) {
        console.error(`WebSocket Error: ${error}`);
    };

    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`WebSocket connection closed cleanly, code=${event.code}, reason=${event.reason}`);
        } else {
            console.error('WebSocket connection died');
        }
    };
}






let rootNode = null;

function updateTree(nodeData) {
    if (!rootNode) {
        rootNode = nodeData;
        renderInitialTree();
    } else {
        addNodeToTree(nodeData);
    }
}

function renderInitialTree() {
    const treeElement = renderTree(rootNode, {
        k: 2,
        depth: 7,
        fill: "#3498db",
        stroke: "#2980b9"
    });
    
    const main_ui = document.getElementById('tree-container');
    main_ui.innerHTML = "";
    main_ui.style.overflow = "auto";
    main_ui.appendChild(treeElement);
}

function addNodeToTree(nodeData) {
    // Find the parent node and add the new node as a child
    function findAndAddNode(node) {
        if (node.text === nodeData.text.slice(0, -nodeData.disp_text.length)) {
            if (!node.children) node.children = [];
            node.children.push(nodeData);
            return true;
        }
        if (node.children) {
            for (let child of node.children) {
                if (findAndAddNode(child)) return true;
            }
        }
        return false;
    }

    findAndAddNode(rootNode);

    // Re-render the tree
    renderInitialTree();
}

function renderTree(rootNode, {
  tree = d3.tree,
  k = 2,
  depth = 2,
  padding = 1,
  r = 3,  // Add this back in
  fill = "#999",
  stroke = "#555",
  strokeWidth = 1.5,
  strokeOpacity = 0.4,
  halo = "#fff",
  haloWidth = 3,
  curve = d3.curveBumpX,
} = {}) {
  const treeContainer = document.getElementById('tree-container');
  treeContainer.innerHTML = ''; // Clear existing content
  const root = d3.hierarchy(rootNode, d => d.children);

  // Compute the layout without fixed dimensions
  const dx = 20;
  const dy = 180; // Adjust this value to control horizontal spacing
  tree().nodeSize([dx, dy])(root);

  // Calculate the bounds of the tree
  let x0 = Infinity;
  let x1 = -x0;
  let y0 = Infinity;
  let y1 = -y0;
  root.each(d => {
    if (d.x > x1) x1 = d.x;
    if (d.x < x0) x0 = d.x;
    if (d.y > y1) y1 = d.y;
    if (d.y < y0) y0 = d.y;
  });

  // Calculate the dimensions of the SVG
  const width = y1 - y0 + dy * 2;
  const height = x1 - x0 + dx * 2;

  const svg = d3.create("svg")
    .attr("viewBox", [y0 - dy, x0 - dx, width, height])
    .attr("style", "width: 100%; height: auto; overflow: visible;")
    .attr("font-family", "sans-serif")
    .attr("font-size", 10);

  svg.append("g")
    .attr("fill", "none")
    .attr("stroke", stroke)
    .attr("stroke-opacity", strokeOpacity)
    .attr("stroke-width", strokeWidth)
    .selectAll("path")
    .data(root.links())
    .join("path")
    .attr("d", d3.link(curve)
      .x(d => d.y)
      .y(d => d.x));

  const node = svg.append("g")
    .selectAll("g")
    .data(root.descendants())
    .join("g")
    .attr("transform", d => `translate(${d.y},${d.x})`);

  node.append("circle")
    .attr("fill", d => d.children ? stroke : fill)
    .attr("r", r);  // Now this should work correctly

  const text = node.append("text")
    .attr("dy", "0.32em")
    .attr("x", d => d.children ? -6 : 6)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .attr("paint-order", "stroke")
    .attr("stroke", halo)
    .attr("stroke-width", haloWidth)
    .style("pointer-events", "all")
    .text(d => d.data.disp_text)
    .on("click", (event, d) => {
      console.log("Clicked node text:", d.data.text);
      console.log("Y location:", d.y);
      console.log("x location:", d.x);
      attribute_text(user_text, d.data.text);
  });

  return svg.node();
}


  function renderTokens(data, tokens) {
    const tokenContainer = document.getElementById('token-container');
    const tooltip = document.getElementById('tooltip');

    // Clear any existing tokens
    tokenContainer.innerHTML = '';

    // Create a span element for each token
    tokens.forEach((token, index) => {
      const tokenElement = document.createElement('span');
      tokenElement.textContent = token;
      tokenElement.classList.add('token');
      tokenElement.addEventListener('mouseover', () => {
        highlightAffectedTokens(index, data, tokens);
        //showTooltip(token);
      });
      tokenElement.addEventListener('mouseout', () => {
        removeHighlight();
        //hideTooltip();
      });
      tokenContainer.appendChild(tokenElement);
    });
  }

  function highlightAffectedTokens(tokenIndex, data, tokens) {
    const tokenElements = document.querySelectorAll('.token');
    tokenElements.forEach((element, index) => {
        const salienceScore = data[tokenIndex][index];
        if (salienceScore > 0){
        element.classList.toggle('highlight', salienceScore > 0);
        element.style.backgroundColor = `rgba(54, 47, 237, ${salienceScore})`;
        }
        else{
        element.classList.remove('highlight');
        element.style.backgroundColor = '';}
      
    });
  }

  function removeHighlight() {
    const tokenElements = document.querySelectorAll('.token');
    tokenElements.forEach(element => {
      element.classList.remove('highlight');
      element.style.backgroundColor = '';
    });
  }

  function showTooltip(token) {
    const tooltip = document.getElementById('tooltip');
    tooltip.textContent = `Hovered Token: ${token}`;
    tooltip.style.display = 'block';
  }

  function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'none';
  }


async function attribute_text(user_text, node_text){
let user_req = `http://127.0.0.1:8000/api/attribute_text/?input_text=${user_text}&node_text=${node_text}`

const response = await fetch(user_req)
const data = await response.json()
const json_data = JSON.parse(data)
const attribution_scores =json_data['data']
console.log(attribution_scores)
console.log(json_data['col_names'])
console.log(json_data['row_names'])


renderTokens(attribution_scores, json_data['row_names']);


}


const example_button_1 = document.getElementById('example-1')
const example_button_2 = document.getElementById('example-2')
const example_button_3 = document.getElementById('example-3')
example_button_1.addEventListener('click', function() {get_tree(example_button_1.innerHTML)})
example_button_2.addEventListener('click', function() {get_tree(example_button_2.innerHTML)})
example_button_3.addEventListener('click', function() {get_tree(example_button_3.innerHTML)})
//example_button_1.onclick = function() {get_tree('Once upon a time there was')}}
}