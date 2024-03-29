html {
  direction:rtl;
}

body {
  font-family: Amiri-Regualr, Helvetica, sans-serif;
  padding: 18px;
  background: #f1f1f1;
  font-size: 14px;
  padding-top: 70px; 
  /* direction: rtl; */

}
@font-face{
font-family: Amiri-Regualr;
src: url('../fonts/Amiri-Regular.ttf');
font-weight: normal;}
@font-face{
font-family: Amiri-Bold;
src: url('../fonts/Amiri-Bold.ttf');
font-weight: normal;}
/* Header/Blog Title */
.header {
  padding: 10px;
  font-size: 20px;
  text-align: center;
  background: white;
  /* direction: rtl; */
 } 

/* navigation menus on top  */
/* .topnav {
  background-color: #b20000;
  /* overflow: hidden; */
  /* direction: rtl; */
  /* position: fixed;
  left: 0;
  top: 0;
  width: 100%; */

/* } */ 

/* Style the links inside the navigation bar */
/* .topnav a {
  float: right;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 18px;
  font-weight: bold;
  direction: rtl;
} */

/* Change the color of links on hover */
/* .topnav a:hover {
  background-color: #ddd;
  color: black;
} */

/* Add a color to the active/current link */
/* .topnav a.active {
  background-color: #0d0d0e;
  color: white;
} */
#footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: black;
  color: white;
  text-align: center;
  direction: ltr;
  
}
#footer a {
  color: white;
}

/* Style the myHeader */
#myHeader {
  padding: 10px 16px;
  background: #607D8B;;
  color: #f1f1f1;
}

/* Page content */
.content {
  padding: 16px;
}

/* The sticky class is added to the header with JS when it reaches its scroll position */
/* .sticky {
  position: fixed;
  top: 0;
  width: 100%
} */

/* Add some top padding to the page content to prevent sudden quick movement (as the header gets a new position at the top of the page (position:fixed and top:0) */
/* .sticky + .content {
  padding-top: 102px;
} */