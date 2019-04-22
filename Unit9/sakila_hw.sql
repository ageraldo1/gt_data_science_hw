/* 
    Comparisons are case insensitive when the column uses a collation which ends with _ci (such as the default latin1_general_ci collation) 
    and they are case sensitive when the column uses a collation which ends with _cs or _bin 
    (such as the utf8_unicode_cs and utf8_bin collations).

    show variables like '%collation%';
    
    Variable_name	          Value
    collation_connection	  latin1_swedish_ci
    collation_database	    latin1_swedish_ci
    collation_server	      latin1_swedish_ci
*/    
    

USE sakila;

-- 1a. Display the first and last names of all actors from the table actor.
SELECT first_name, last_name 
  FROM actor;
  
-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT CONCAT(first_name, ' ',  last_name) as 'Actor Name'
  FROM actor;
  
-- 2a. You need to find the ID number, first name, and last name of an actor, 
-- of whom you know only the first name, "Joe." 
-- What is one query would you use to obtain this information?   
SELECT actor_id, first_name, last_name 
  FROM actor
     WHERE first_name = 'Joe';


-- 2b. Find all actors whose last name contain the letters GEN:
SELECT actor_id, first_name, last_name
   FROM actor
      WHERE last_name like '%GEN%';
      
-- 2c. Find all actors whose last names contain the letters LI. 
-- This time, order the rows by last name and first name, in that order:      
SELECT actor_id, first_name, last_name
  FROM actor
     WHERE last_name like '%LI%'
ORDER BY last_name, first_name;

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China
SELECT country_id, country
  FROM country
     WHERE country in ('Afghanistan', 'Bangladesh', 'China');
     
-- 3a. You want to keep a description of each actor. You don't think you will be performing queries on a description, 
-- so create a column in the table actor named description and use the data type BLOB 
-- (Make sure to research the type BLOB, as the difference between it and VARCHAR are significant).     
ALTER TABLE actor ADD description BLOB AFTER last_update;

-- 3b. Very quickly you realize that entering descriptions for each actor is too much effort. Delete the description column.
ALTER TABLE actor DROP COLUMN description;

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT last_name, COUNT(last_name) as 'Last Name Count'
  FROM actor
GROUP BY last_name;  


-- 4b. List last names of actors and the number of actors who have that last name, 
-- but only for names that are shared by at least two actors
SELECT last_name, COUNT(last_name) as 'Last Name Count'
  FROM actor
GROUP BY last_name  
HAVING COUNT(last_name) >1;

-- 4c. The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS. Write a query to fix the record.
SELECT first_name, last_name 
  FROM actor
     WHERE first_name = 'GROUCHO'
       AND last_name  = 'WILLIAMS';

UPDATE actor
SET first_name = 'HARPO', 
    last_name  = 'WILLIAMS'
WHERE first_name = 'GROUCHO'
  AND last_name  = 'WILLIAMS';
  
-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. 
-- It turns out that GROUCHO was the correct name after all! 
-- In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO.  
UPDATE actor
   SET first_name = 'GROUCHO'
      WHERE first_name = 'HARPO';
      
-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;


CREATE TABLE IF NOT EXISTS `address` (
  `address_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `address` varchar(50) NOT NULL,
  `address2` varchar(50) DEFAULT NULL,
  `district` varchar(20) NOT NULL,
  `city_id` smallint(5) unsigned NOT NULL,
  `postal_code` varchar(10) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `location` geometry NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`address_id`),
  KEY `idx_fk_city_id` (`city_id`),
  SPATIAL KEY `idx_location` (`location`),
  CONSTRAINT `fk_address_city` FOREIGN KEY (`city_id`) REFERENCES `city` (`city_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=606 DEFAULT CHARSET=utf8;

DESCRIBE address;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address
SELECT s.first_name, s.last_name, a.address
  FROM staff s, address a
     where s.address_id = a.address_id;
     
-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.     
SELECT CONCAT(s.first_name, ' ', s.last_name) as 'Staff Member', SUM(p.amount) as 'Amount Rung Up'
  FROM staff s, payment p
     WHERE s.staff_id = p.staff_id
       AND (MONTH(p.payment_date) = 8 AND YEAR(p.payment_date) = 2005)
GROUP BY s.first_name, s.last_name;

-- 6c. List each film and the number of actors who are listed for that film. 
-- Use tables film_actor and film. Use inner join.
SELECT f.title as 'Film', COUNT(fa.film_id) as 'Number of Actors'
  FROM film f, film_actor fa
     WHERE f.film_id = fa.film_id
GROUP BY f.title;


-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
SELECT COUNT(*) as 'Total Copies'
  FROM film f, inventory i 
     WHERE f.title   = 'HUNCHBACK IMPOSSIBLE'
       AND f.film_id = i.film_id;
       
-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. 
-- List the customers alphabetically by last name:       
SELECT c.first_name, c.last_name, SUM(p.amount) AS 'Total Amount Paid'
  FROM customer c, payment p
     WHERE c.customer_id = p.customer_id
GROUP BY c.first_name, c.last_name     
ORDER BY c.last_name;  

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
-- As an unintended consequence, films starting with the letters K and Q have also soared in popularity. 
-- Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.
SELECT f.title
 FROM film f
    WHERE (f.title LIKE 'K%' OR f.title LIKE 'Q%')
      AND f.language_id = (SELECT l.language_id
                             FROM language l
                                WHERE l.name = 'English'
                                  AND f.language_id = l.language_id
                          );
                          
-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
SELECT CONCAT(first_name, ' ', last_name) AS 'Actor'
  FROM actor 
     WHERE actor_id IN (SELECT fa.actor_id
                          FROM film_actor fa, film f
                             WHERE f.title = 'ALONE TRIP'
                               AND f.film_id = fa.film_id
                       );
  
  
-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. 
-- Use joins to retrieve this information.
SELECT c.first_name, c.last_name, c.email
  FROM customer c, address a, city ct, country co
     WHERE c.active       = TRUE
        AND c.address_id  = a.address_id
        AND a.city_id     = ct.city_id
        AND ct.country_id = co.country_id
        AND co.country    = 'CANADA';
        
        
-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. 
-- Identify all movies categorized as family films.        
SELECT f.title
  FROM film f, film_category fc, category c
     WHERE f.film_id      = fc.film_id
       AND fc.category_id = c.category_id
       AND c.name         = 'Family';
       
-- 7e. Display the most frequently rented movies in descending order       
SELECT f.title, COUNT(r.rental_date)
  FROM film f, inventory i, rental r
     WHERE f.film_id      = i.film_id
       AND i.inventory_id = r.inventory_id
GROUP BY f.title
ORDER BY COUNT(r.rental_date) DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT i.store_id AS 'StoreID', CONCAT(c.city, ',', co.country) AS 'Store Location', SUM(p.amount) AS 'Total Sales'
  FROM payment p, rental r, inventory i, store s, address a, city c, country co
      WHERE p.rental_id    = r.rental_id
        AND r.inventory_id = i.inventory_id
        AND i.store_id     = s.store_id
        AND s.address_id   = a.address_id
        AND a.city_id      = c.city_id
        AND c.country_id   = co.country_id
GROUP BY i.store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT store_id AS 'Store ID', c.city, co.country
  FROM store s, address a, city c, country co
     WHERE s.address_id = a.address_id
       AND a.city_id    = c.city_id
       AND c.country_id = co.country_id;
       
-- 7h. List the top five genres in gross revenue in descending order. 
-- (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)
SELECT c.name AS 'Genre', SUM(p.amount) AS 'Gross Revenue'
  FROM payment p, rental r, inventory i, film f, film_category fc, category c
     WHERE p.rental_id    = r.rental_id
       AND r.inventory_id = i.inventory_id
       AND i.film_id      = f.film_id
       AND f.film_id      = fc.film_id
       AND fc.category_id = c.category_id
GROUP BY c.name     
ORDER BY SUM(p.amount) DESC
LIMIT 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. 
-- Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW Top5_Genres_Gross_Revenue AS
SELECT c.name AS 'Genre', SUM(p.amount) AS 'Gross Revenue'
  FROM payment p, rental r, inventory i, film f, film_category fc, category c
     WHERE p.rental_id    = r.rental_id
       AND r.inventory_id = i.inventory_id
       AND i.film_id      = f.film_id
       AND f.film_id      = fc.film_id
       AND fc.category_id = c.category_id
GROUP BY c.name     
ORDER BY SUM(p.amount) DESC
LIMIT 5;

-- 8b. How would you display the view that you created in 8a?
SELECT * 
  FROM Top5_Genres_Gross_Revenue;
  
-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.  
DROP VIEW IF EXISTS Top5_Genres_Gross_Revenue;

       
