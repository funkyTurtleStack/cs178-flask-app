-- Create the database
CREATE DATABASE IF NOT EXISTS ProjectOneStore;
USE ProjectOneStore;

-- Create the Category table
CREATE TABLE IF NOT EXISTS Category (
    categoryID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create the Inventory table
CREATE TABLE IF NOT EXISTS Inventory (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    categoryID INT,
    FOREIGN KEY (categoryID) REFERENCES Category(categoryID)
);

-- Insert categories into Category table
INSERT INTO Category (name) VALUES ('Toys'), ('Kitchen'), ('Furniture');

-- Insert items into Inventory table
-- Assuming categoryID for Toys = 1, Kitchen = 2, Furniture = 3
INSERT INTO Inventory (description, price, categoryID) VALUES 
('Toy Car', 9.99, 1),
('Doll House', 24.99, 1),
('Building Blocks', 19.99, 1),
('Kitchen Knife Set', 29.99, 2),
('Non-stick Pan', 17.99, 2),
('Blender', 35.99, 2),
('Dining Table', 199.99, 3),
('Sofa', 399.99, 3),
('Chair', 49.99, 3),
('Bookshelf', 89.99, 3),
('Action Figure', 14.99, 1),
('Puzzle Game', 12.99, 1),
('Remote Control Car', 29.99, 1),
('Coffee Maker', 45.99, 2),
('Toaster', 19.99, 2),
('Cutting Board', 9.99, 2),
('Desk', 109.99, 3),
('Wardrobe', 249.99, 3),
('Bed Frame', 149.99, 3),
('Teddy Bear', 15.99, 1),
('Lego Set', 59.99, 1),
('Board Game', 34.99, 1),
('Jigsaw Puzzle', 10.99, 1),
('Play Kitchen', 89.99, 1),
('Microwave Oven', 99.99, 2),
('Mixing Bowl Set', 24.99, 2),
('Electric Kettle', 29.99, 2),
('Dish Rack', 15.99, 2),
('Spice Rack', 20.99, 2),
('Nightstand', 39.99, 3),
('Office Chair', 75.99, 3),
('Coffee Table', 55.99, 3),
('Floor Lamp', 42.99, 3),
('TV Stand', 129.99, 3);