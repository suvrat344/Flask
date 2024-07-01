# Creating HTML files with Jinja

Learners will be given a data set in the form of a python array. The data consists of product information like, *product_id, Product_Name, type* and *producer* which is to be retrieved and organized. 

Create an HTML template such that it segregates the given data according to *producer* of the product.

Steps to carry out this activity are given below:

- Copy the Product data in the python file *main.py* from the *Products.txt* file provided
- Create an external file that contains the HTML template which can be opened in our python file
     1. The template should be able to segregate the product data in **sections** with respect to its *producer*, and display information in the form of table with their producer as the heading.
     2. The table columns should display product_id, name and their type.
     2. Finally, the HTML file should display a brief (one sentence) information about the number of entries in each section formed     
- With the help of jinja2, render the complete information as an HTML file.
- Save this HTML file as *index.html* as an external file in the in the working directory.
- Any change in the data provided should overwrite the existing HTML file and should NOT create a new HTML file in that folder.
- things to learn: basic templating, filters.
 
Note: Same steps can be followed to segreted the table with respect to *type*
