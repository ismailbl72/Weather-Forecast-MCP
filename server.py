# 🏋️‍♂️ FitPersona - Kişiye Özel Spor ve BMI Asistanı MCP Server
from mcp.server.fastmcp import FastMCP
from app import (
    calculate_bmi,
    get_nutrition_advice,
    get_exercise_plan,
    get_weekly_schedule
)

# Initialize FitPersona MCP server
mcp = FastMCP("fitpersona-mcp")

@mcp.tool()
async def calculate_user_bmi(height_cm: float, weight_kg: float) -> dict:
    """
    Kullanıcının boy ve kilo bilgisine göre BMI hesaplar.

    Args:
        height_cm: Boy (santimetre cinsinden, örn: 175)
        weight_kg: Kilo (kilogram cinsinden, örn: 70)

    Returns:
        BMI değeri, kategori ve öneriler
    """
    result = calculate_bmi(height_cm, weight_kg)
    return result

@mcp.tool()
async def get_personalized_nutrition(
    height_cm: float,
    weight_kg: float,
    gender: str,
    age: int,
    activity_level: str = "orta"
) -> dict:
    """
    Kişisel bilgilere göre beslenme önerileri ve kalori hedefi verir.

    Args:
        height_cm: Boy (santimetre)
        weight_kg: Kilo (kilogram)
        gender: Cinsiyet ("erkek" veya "kadın")
        age: Yaş
        activity_level: Aktivite seviyesi ("düşük", "orta", "yüksek")

    Returns:
        Beslenme önerileri, kalori hedefi ve BMI bilgisi
    """
    # Önce BMI hesapla
    bmi_result = calculate_bmi(height_cm, weight_kg)
    if "error" in bmi_result:
        return bmi_result

    bmi = bmi_result["bmi"]

    # Beslenme önerilerini al
    nutrition_result = get_nutrition_advice(bmi, gender, age, activity_level)

    # BMI bilgisini de ekle
    if "error" not in nutrition_result:
        nutrition_result["bmi_info"] = bmi_result

    return nutrition_result

@mcp.tool()
async def get_personalized_exercise(
    height_cm: float,
    weight_kg: float,
    gender: str,
    age: int,
    fitness_goal: str = "auto"
) -> dict:
    """
    Kişisel bilgilere göre egzersiz planı önerir.

    Args:
        height_cm: Boy (santimetre)
        weight_kg: Kilo (kilogram)
        gender: Cinsiyet ("erkek" veya "kadın")
        age: Yaş
        fitness_goal: Hedef ("kilo_verme", "kas_yapma", "form_koruma", "auto")

    Returns:
        Kişiselleştirilmiş egzersiz planı ve BMI bilgisi
    """
    # Önce BMI hesapla
    bmi_result = calculate_bmi(height_cm, weight_kg)
    if "error" in bmi_result:
        return bmi_result

    bmi = bmi_result["bmi"]

    # Egzersiz planını al
    exercise_result = get_exercise_plan(bmi, gender, age, fitness_goal)

    # BMI bilgisini de ekle
    if "error" not in exercise_result:
        exercise_result["bmi_info"] = bmi_result

    return exercise_result

@mcp.tool()
async def get_weekly_workout_schedule(fitness_goal: str = "form_koruma", intensity: str = "orta") -> dict:
    """
    Haftalık detaylı antrenman programı oluşturur.

    Args:
        fitness_goal: Fitness hedefi ("kilo_verme", "kas_yapma", "form_koruma")
        intensity: Yoğunluk seviyesi ("düşük", "orta", "yüksek")

    Returns:
        7 günlük detaylı antrenman programı
    """
    result = get_weekly_schedule(fitness_goal, intensity)
    return result

@mcp.tool()
async def get_complete_fitness_plan(
    height_cm: float,
    weight_kg: float,
    gender: str,
    age: int,
    activity_level: str = "orta",
    fitness_goal: str = "auto"
) -> dict:
    """
    Komple fitness planı - BMI, beslenme ve egzersiz önerilerini birleştirir.

    Args:
        height_cm: Boy (santimetre)
        weight_kg: Kilo (kilogram)
        gender: Cinsiyet ("erkek" veya "kadın")
        age: Yaş
        activity_level: Aktivite seviyesi ("düşük", "orta", "yüksek")
        fitness_goal: Hedef ("kilo_verme", "kas_yapma", "form_koruma", "auto")

    Returns:
        Komple kişiselleştirilmiş fitness planı
    """
    # BMI hesapla
    bmi_result = calculate_bmi(height_cm, weight_kg)
    if "error" in bmi_result:
        return bmi_result

    bmi = bmi_result["bmi"]

    # Beslenme önerilerini al
    nutrition_result = get_nutrition_advice(bmi, gender, age, activity_level)

    # Egzersiz planını al
    exercise_result = get_exercise_plan(bmi, gender, age, fitness_goal)

    # Haftalık programı al
    weekly_result = get_weekly_schedule(
        exercise_result.get("fitness_goal", fitness_goal),
        exercise_result.get("intensity_level", "orta")
    )

    # Tüm sonuçları birleştir
    complete_plan = {
        "user_profile": {
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "gender": gender,
            "age": age,
            "activity_level": activity_level
        },
        "bmi_analysis": bmi_result,
        "nutrition_plan": nutrition_result,
        "exercise_plan": exercise_result,
        "weekly_schedule": weekly_result,
        "status": "success"
    }

    return complete_plan

if __name__ == "__main__":
    mcp.run(transport="stdio")