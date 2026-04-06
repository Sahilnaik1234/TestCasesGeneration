package com.example.inventory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class InventoryManager {

    private Map<String, Item> inventory = new HashMap<>();
    private List<String> transactionLog = new ArrayList<>();
    private double totalRevenue = 0.0;

    public static class Item {
        private String id;
        private String name;
        private int quantity;
        private double price;
        private String category;

        public Item(String id, String name, int quantity, double price, String category) {
            this.id = id;
            this.name = name;
            this.quantity = quantity;
            this.price = price;
            this.category = category;
        }

        public String getId() { return id; }
        public String getName() { return name; }
        public int getQuantity() { return quantity; }
        public void setQuantity(int quantity) { this.quantity = quantity; }
        public double getPrice() { return price; }
        public void setPrice(double price) { this.price = price; }
        public String getCategory() { return category; }
    }

    public void addItem(String id, String name, int quantity, double price, String category) {
        if (id == null || id.trim().isEmpty()) {
            throw new IllegalArgumentException("Item ID cannot be null or empty");
        }
        if (price < 0 || quantity < 0) {
            throw new IllegalArgumentException("Price and quantity must be non-negative");
        }

        if (inventory.containsKey(id)) {
            Item existingItem = inventory.get(id);
            existingItem.setQuantity(existingItem.getQuantity() + quantity);
            logTransaction("Updated quantity for item: " + id);
        } else {
            Item newItem = new Item(id, name, quantity, price, category);
            inventory.put(id, newItem);
            logTransaction("Added new item to inventory: " + id);
        }
    }

    public void removeItem(String id) {
        if (!inventory.containsKey(id)) {
            throw new IllegalArgumentException("Item not found in inventory: " + id);
        }
        inventory.remove(id);
        logTransaction("Removed item from inventory: " + id);
    }

    public void updateItemPrice(String id, double newPrice) {
        if (!inventory.containsKey(id)) {
            throw new IllegalArgumentException("Item not found in inventory: " + id);
        }
        if (newPrice < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
        inventory.get(id).setPrice(newPrice);
        logTransaction("Updated price for item " + id + " to " + newPrice);
    }

    public boolean processSale(String id, int quantitySold) {
        if (!inventory.containsKey(id)) {
            return false;
        }

        Item item = inventory.get(id);
        if (item.getQuantity() < quantitySold) {
            return false;
        }

        item.setQuantity(item.getQuantity() - quantitySold);
        double saleValue = quantitySold * item.getPrice();
        totalRevenue += saleValue;
        
        logTransaction("Sold " + quantitySold + " of " + id + " for " + saleValue);
        
        if (item.getQuantity() == 0) {
            logTransaction("Item " + id + " is now out of stock.");
        }
        
        return true;
    }

    public Item getItem(String id) {
        return inventory.get(id);
    }

    public List<Item> getItemsByCategory(String category) {
        return inventory.values().stream()
            .filter(item -> item.getCategory().equalsIgnoreCase(category))
            .collect(Collectors.toList());
    }

    public double calculateTotalInventoryValue() {
        return inventory.values().stream()
            .mapToDouble(item -> item.getQuantity() * item.getPrice())
            .sum();
    }

    public List<Item> getLowStockItems(int threshold) {
        return inventory.values().stream()
            .filter(item -> item.getQuantity() <= threshold)
            .collect(Collectors.toList());
    }

    public double getTotalRevenue() {
        return totalRevenue;
    }

    public List<String> getTransactionLog() {
        return new ArrayList<>(transactionLog);
    }

    private void logTransaction(String message) {
        String logEntry = System.currentTimeMillis() + ": " + message;
        transactionLog.add(logEntry);
        // Ensure log doesn't grow indefinitely in this mock
        if (transactionLog.size() > 500) {
            transactionLog.remove(0);
        }
    }
    
    public void printInventoryStatus() {
        System.out.println("--- Current Inventory Status ---");
        for (Item item : inventory.values()) {
            System.out.printf("ID: %s | Name: %s | Qty: %d | Price: $%.2f | Category: %s%n",
                item.getId(), item.getName(), item.getQuantity(), item.getPrice(), item.getCategory());
        }
        System.out.println("Total Inventory Value: $" + calculateTotalInventoryValue());
        System.out.println("Total Revenue: $" + totalRevenue);
        System.out.println("--------------------------------");
    }
}
