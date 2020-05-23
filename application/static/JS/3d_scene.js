text = document.getElementById("overlay");
var opacity = 0;

//creating a scene and a camera
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

//creating renderer and attaching to body canvas
var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

//geometry creation
//BOX1
var geometry = new THREE.BoxGeometry();
var material = new THREE.MeshBasicMaterial( { color : 0xffffff } );
var cube = new THREE.Mesh(geometry, material);
scene.add(cube);

//simple axis object
//var axesHelper = new THREE.AxesHelper( 5 );
//scene.add( axesHelper );

camera.position.z = 2;

//logic for movements
var update = function() {

};

//render the whole scene and postprocess
var render = function() {
	renderer.render( scene, camera );
};

//this runs everything and refreshes screen based on the screen refresh rate of target
function MainLoop() {
	requestAnimationFrame( MainLoop );
	//object animations here
	//BOX1 animation
	if(cube.position.y >= -.5) {
		cube.translateY(-.01);
		opacity += .02;
	} else {
		cube.rotation.x += 0.01;
		cube.rotation.z += 0.01;
	}

	text.style.opacity = opacity;
	console.log(opacity);
	update();
	render();
}
MainLoop();