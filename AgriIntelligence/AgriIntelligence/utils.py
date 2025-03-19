import os
import json
import numpy as np
from PIL import Image

# Define allowed file extensions for image uploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_disease(image_path, plant_type):
    """
    Predict plant disease from image
    
    In a real implementation, this would use a TensorFlow/Keras model.
    For simplicity, we're providing a placeholder implementation that returns predefined results.
    """
    try:
        # Load and preprocess the image
        img = Image.open(image_path)
        img = img.resize((224, 224))  # Resize to match model input
        
        # Here you would normally:
        # 1. Convert the image to a numpy array
        # 2. Preprocess it for your model
        # 3. Make a prediction using a trained model
        
        # Simplified mock implementation with common plant diseases
        diseases_by_plant = {
            'tomato': ['Early Blight', 'Late Blight', 'Leaf Mold', 'Healthy'],
            'potato': ['Early Blight', 'Late Blight', 'Blackleg', 'Healthy'],
            'corn': ['Gray Leaf Spot', 'Common Rust', 'Northern Leaf Blight', 'Healthy'],
            'rice': ['Brown Spot', 'Leaf Blast', 'Bacterial Leaf Blight', 'Healthy'],
            'wheat': ['Leaf Rust', 'Powdery Mildew', 'Septoria', 'Healthy'],
        }
        
        # Get possible diseases for the plant type
        possible_diseases = diseases_by_plant.get(plant_type.lower(), ['Unknown', 'Healthy'])
        
        # For simulation, we'll choose one of the diseases based on the image characteristics
        # In a real implementation, this would be the output of your ML model
        img_array = np.array(img)
        avg_pixel_value = np.mean(img_array)
        
        # Use the average pixel value to select a disease (just for simulation)
        disease_index = int(avg_pixel_value) % len(possible_diseases)
        disease = possible_diseases[disease_index]
        
        # Generate a confidence score (this would come from your model in a real implementation)
        confidence = 0.7 + 0.2 * (np.random.random())  # Random confidence between 0.7 and 0.9
        
        return disease, confidence
        
    except Exception as e:
        print(f"Error predicting disease: {str(e)}")
        return "Error processing image", 0.0


def recommend_crops(soil_type, climate, temperature, humidity, rainfall, ph):
    """
    Recommend crops based on soil and climate conditions
    
    In a real implementation, this would use a data-driven approach with a model or database.
    For simplicity, we're using predefined recommendations.
    """
    # Dictionary of suitable crops by soil type and climate
    crop_suitability = {
        'clay': {
            'tropical': ['rice', 'sugarcane', 'cotton'],
            'subtropical': ['wheat', 'cabbage', 'broccoli'],
            'temperate': ['barley', 'peas', 'beans'],
            'arid': ['safflower', 'sorghum', 'cotton']
        },
        'sandy': {
            'tropical': ['coconut', 'cashew', 'groundnut'],
            'subtropical': ['watermelon', 'muskmelon', 'sweet potato'],
            'temperate': ['potato', 'carrots', 'radish'],
            'arid': ['millet', 'sesame', 'cowpea']
        },
        'loamy': {
            'tropical': ['banana', 'coffee', 'tobacco'],
            'subtropical': ['maize', 'wheat', 'pulses'],
            'temperate': ['oats', 'rye', 'potato'],
            'arid': ['maize', 'sunflower', 'pearl millet']
        },
        'silty': {
            'tropical': ['sugarcane', 'rice', 'jute'],
            'subtropical': ['corn', 'soybean', 'wheat'],
            'temperate': ['pumpkin', 'lettuce', 'cucumber'],
            'arid': ['sorghum', 'barley', 'wheat']
        },
        'peaty': {
            'tropical': ['vegetables', 'rice', 'sugarcane'],
            'subtropical': ['corn', 'celery', 'onion'],
            'temperate': ['beets', 'potatoes', 'lettuce'],
            'arid': ['not suitable for arid conditions']
        }
    }
    
    # Get base recommendations by soil and climate
    base_recommendations = crop_suitability.get(soil_type.lower(), {}).get(climate.lower(), ['wheat', 'rice', 'corn'])
    
    # Additional crops based on pH
    ph_based_crops = []
    if ph < 5.5:  # Acidic soil
        ph_based_crops = ['blueberry', 'potato', 'rye']
    elif 5.5 <= ph <= 7.0:  # Neutral soil
        ph_based_crops = ['corn', 'wheat', 'soybean']
    else:  # Alkaline soil
        ph_based_crops = ['alfalfa', 'asparagus', 'cabbage']
    
    # Additional recommendations based on temperature and rainfall
    # These would be more sophisticated in a real system
    climate_crops = []
    
    if temperature > 25 and rainfall > 1000:  # Hot and wet
        climate_crops = ['rice', 'sugarcane', 'banana']
    elif temperature > 25 and rainfall <= 1000:  # Hot and dry
        climate_crops = ['millet', 'sorghum', 'cotton']
    elif temperature <= 25 and rainfall > 1000:  # Cool and wet
        climate_crops = ['lettuce', 'cabbage', 'peas']
    else:  # Cool and dry
        climate_crops = ['wheat', 'barley', 'oats']
    
    # Combine all recommendations, remove duplicates
    all_recommendations = list(set(base_recommendations + ph_based_crops + climate_crops))
    
    # For each crop, add some details about why it was recommended
    detailed_recommendations = []
    for crop in all_recommendations:
        details = {
            'name': crop.capitalize(),
            'suitability': 'High' if crop in base_recommendations else 'Medium',
            'reasons': []
        }
        
        if crop in base_recommendations:
            details['reasons'].append(f"Suitable for {soil_type} soil in {climate} climate")
        if crop in ph_based_crops:
            details['reasons'].append(f"Appropriate for soil pH of {ph}")
        if crop in climate_crops:
            details['reasons'].append(f"Well-adapted to temperature of {temperature}°C and rainfall of {rainfall}mm")
            
        detailed_recommendations.append(details)
    
    return detailed_recommendations


def recommend_irrigation(crop_type, soil_type, area_size, climate, temperature, humidity, rainfall):
    """
    Generate irrigation recommendations based on crop, soil, and climate conditions
    
    Parameters:
    - crop_type: Type of crop
    - soil_type: Type of soil
    - area_size: Size of area in square meters
    - climate: Climate type
    - temperature: Temperature in Celsius
    - humidity: Humidity percentage
    - rainfall: Rainfall in mm
    
    Returns:
    - recommendation: Text recommendation
    - water_requirement: Water requirement in liters
    - schedule: Irrigation schedule
    """
    # Base water requirements by crop (liters per square meter per day)
    crop_water_req = {
        'rice': 8.0,
        'wheat': 4.5,
        'corn': 5.5,
        'potato': 4.0,
        'tomato': 3.5,
        'lettuce': 3.0,
        'carrot': 2.5,
        'onion': 2.0,
        'beans': 3.0,
        'peas': 2.5,
        'cotton': 6.0,
        'sugarcane': 7.0,
    }
    
    # Soil type efficiency factors (how much water is retained)
    soil_factors = {
        'clay': 0.8,  # Retains water well
        'sandy': 1.5,  # Drains quickly, needs more water
        'loamy': 1.0,  # Balanced water retention
        'silty': 0.9,  # Good water retention
        'peaty': 0.7,  # High water retention
    }
    
    # Climate adjustment factors
    climate_factors = {
        'tropical': 1.2,
        'subtropical': 1.1,
        'temperate': 0.9,
        'arid': 1.3,
    }
    
    # Get base water requirement per day
    base_req = crop_water_req.get(crop_type.lower(), 5.0)  # Default to 5L if crop not found
    
    # Apply soil factor
    soil_factor = soil_factors.get(soil_type.lower(), 1.0)
    
    # Apply climate factor
    climate_factor = climate_factors.get(climate.lower(), 1.0)
    
    # Adjust for temperature (increase 5% for each degree above 25°C)
    temp_factor = 1.0 + max(0, (temperature - 25) * 0.05)
    
    # Adjust for humidity (decrease 2% for each percentage point above 60%)
    humidity_factor = 1.0 - max(0, (humidity - 60) * 0.02)
    
    # Adjust for rainfall (decrease based on rainfall)
    # Assuming rainfall is in mm per week
    rainfall_adjustment = max(0, 1.0 - (rainfall / 25.0))  # If 25mm or more rain, no irrigation needed
    
    # Calculate daily water requirement per square meter
    daily_req_per_sqm = base_req * soil_factor * climate_factor * temp_factor * humidity_factor * rainfall_adjustment
    
    # Calculate total daily water requirement for the area
    total_daily_req = daily_req_per_sqm * area_size
    
    # Create a weekly schedule
    schedule = []
    for day in range(7):
        # Vary the requirement slightly by day for more realistic schedule
        daily_variation = 0.9 + 0.2 * np.random.random()
        day_req = round(total_daily_req * daily_variation, 1)
        
        # Determine if irrigation is needed today (assume no irrigation on heavy rain days)
        irrigate_today = True
        if rainfall > 10 and day % 2 == 0:  # Simplistic rain pattern
            irrigate_today = False
            
        schedule.append({
            'day': day + 1,
            'water_amount': day_req if irrigate_today else 0,
            'irrigate': irrigate_today,
            'note': 'Rest day due to rainfall' if not irrigate_today else 'Regular irrigation'
        })
    
    # Calculate weekly total
    weekly_total = sum(day['water_amount'] for day in schedule)
    
    # Generate text recommendation
    recommendation = f"For {crop_type} planted in {soil_type} soil in a {climate} climate, "
    recommendation += f"we recommend approximately {round(weekly_total)} liters of water per week "
    recommendation += f"for your {area_size} square meter field."
    
    if rainfall_adjustment < 0.5:
        recommendation += " Due to recent rainfall, irrigation requirements are reduced."
    
    if soil_type == 'sandy':
        recommendation += " Sandy soil drains quickly, so more frequent irrigation with smaller amounts is advised."
    elif soil_type == 'clay':
        recommendation += " Clay soil retains water well, so less frequent irrigation with larger amounts is recommended."
        
    return recommendation, weekly_total, schedule
