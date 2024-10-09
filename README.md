# High-Level Design of Clothing Recommendation System

## Overview:

This system gives you clothing and gear recommendations based on your travel destination, the weather at that location, and the activities you’ll be doing. It processes your input, gets weather data, and then provides suggestions based on predefined rules.

![image](https://github.com/user-attachments/assets/926caba1-0f90-446c-a1d1-765e313c21a3)

## How the System Works:

### User Input:

You provide a sentence, like: 
> "I’m going to Goa for 3 days. I’ll attend a meeting, then swim and run on the beach."

### Understanding the Input:

The system breaks your sentence down to understand three key things:

- **City**: Where you're going (e.g., Goa)
- **Days**: How long you're staying (e.g., 3 days)
- **Activities**: What you’ll be doing (e.g., attending a meeting, swimming, running)

### Weather Data:

Once the system knows the city (e.g., Goa), it checks the current weather there. It gets the temperature, humidity, and if it's going to rain.

### Making Recommendations:

Based on the weather and activities, the system suggests what to wear or bring:

- **Weather-based suggestions**: Light clothes if it's hot, rain gear if it’s raining.
- **Activity-based suggestions**: Swimwear and extra clothes for swimming, running shoes for running.
- **Location-specific suggestions**: For coastal areas, it recommends things like sunscreen and extra water.

### Example:

If you say: 
> "I’m going to Goa to swim and run on the beach,"

the system:

1. Recognizes Goa as the city.
2. Identifies "swim" and "run" as activities.
3. Checks the weather in Goa and gives you recommendations like:

   - **Clothes**: Light clothing, sandals
   - **Extras**: Sunscreen, extra water
   - **For swimming**: Swimwear and extra clothes
   - **For running**: Running shoes and breathable clothes

This process helps the system give relevant recommendations based on where you're going, what you’ll be doing, and the local weather conditions.
