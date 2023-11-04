const mongoose = require("mongoose");

// Define Schemes
const itemsSchema = new mongoose.Schema(
  {
    _id: { type: mongoose.Schema.Types.ObjectId },
    categories: { type: String },
    title: { type: String },
    page_link: { type: String },
    purchase_link: { type: String },
    prices: { type: String },
    members: { type: String },
    date: { type: String },
    contents: { type: String },
    images: { type: mongoose.Schema.Types.Mixed },
  },
  {
    collection: "items",
  }
);

// Create Model & Export
module.exports = mongoose.model("Items", itemsSchema);
