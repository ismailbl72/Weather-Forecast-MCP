# 🏋️‍♂️ FitPersona - Kişiye Özel Spor ve BMI Asistanı
# BMI hesaplama ve fitness önerileri için fonksiyonlar

def calculate_bmi(height_cm: float, weight_kg: float) -> dict:
    """
    Vücut kitle indeksini (BMI) hesaplar.

    Args:
        height_cm: Boy (santimetre)
        weight_kg: Kilo (kilogram)

    Returns:
        BMI değeri ve kategori bilgisi
    """
    try:
        # BMI = kilo (kg) / boy (m)²
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        # BMI kategorisini belirle
        category = get_bmi_category(bmi)

        return {
            "bmi": round(bmi, 1),
            "category": category,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "status": "success"
        }
    except Exception as e:
        return {"error": f"BMI hesaplama hatası: {str(e)}"}

def get_bmi_category(bmi: float) -> dict:
    """
    BMI değerine göre kategori belirler.

    Args:
        bmi: BMI değeri

    Returns:
        Kategori bilgisi ve açıklama
    """
    if bmi < 18.5:
        return {
            "category": "Zayıf",
            "description": "Normal kilodan düşük",
            "recommendation": "Kilo almanız önerilir"
        }
    elif 18.5 <= bmi < 25:
        return {
            "category": "Normal",
            "description": "İdeal kilo aralığında",
            "recommendation": "Mevcut kilonuzu koruyun"
        }
    elif 25 <= bmi < 30:
        return {
            "category": "Fazla Kilolu",
            "description": "Normal kilodan yüksek",
            "recommendation": "Kilo vermeniz önerilir"
        }
    else:
        return {
            "category": "Obez",
            "description": "Obezite sınıfında",
            "recommendation": "Acil kilo vermeniz gerekiyor"
        }

def get_nutrition_advice(bmi: float, gender: str, age: int, activity_level: str = "orta") -> dict:
    """
    BMI ve kişisel bilgilere göre beslenme önerileri verir.

    Args:
        bmi: BMI değeri
        gender: Cinsiyet ("erkek" veya "kadın")
        age: Yaş
        activity_level: Aktivite seviyesi ("düşük", "orta", "yüksek")

    Returns:
        Beslenme önerileri ve kalori hedefi
    """
    try:
        # Temel metabolizma hızı hesaplama (Harris-Benedict formülü)
        if gender.lower() == "erkek":
            bmr = 88.362 + (13.397 * 70) + (4.799 * 170) - (5.677 * age)  # Ortalama değerler
        else:
            bmr = 447.593 + (9.247 * 60) + (3.098 * 160) - (4.330 * age)  # Ortalama değerler

        # Aktivite çarpanı
        activity_multipliers = {
            "düşük": 1.2,
            "orta": 1.55,
            "yüksek": 1.9
        }

        daily_calories = bmr * activity_multipliers.get(activity_level, 1.55)

        # BMI'ye göre kalori hedefi ayarlama
        if bmi < 18.5:
            # Kilo alma için kalori artışı
            target_calories = daily_calories + 300
            goal = "Kilo Alma"
            advice = [
                "🍎 Günde 5-6 öğün yiyin",
                "🥜 Sağlıklı yağlar tüketin (fındık, avokado)",
                "🍗 Protein alımını artırın",
                "🍌 Karbonhidrat alımını artırın",
                "💧 Bol su için (günde 2-3 litre)"
            ]
        elif bmi >= 25:
            # Kilo verme için kalori açığı
            target_calories = daily_calories - 500
            goal = "Kilo Verme"
            advice = [
                "🥗 Sebze ağırlıklı beslenin",
                "🍗 Yağsız protein kaynaklarını tercih edin",
                "🚫 Şekerli içeceklerden kaçının",
                "🍞 Rafine karbonhidratları sınırlayın",
                "💧 Yemeklerden önce su için",
                "⏰ Aralıklı oruç deneyin (16:8)"
            ]
        else:
            # Kilo koruma
            target_calories = daily_calories
            goal = "Kilo Koruma"
            advice = [
                "⚖️ Dengeli beslenin",
                "🍎 Günde 5 porsiyon meyve-sebze",
                "🍗 Kaliteli protein alın",
                "🌾 Tam tahıl ürünlerini tercih edin",
                "💧 Günde 2-3 litre su için"
            ]

        return {
            "goal": goal,
            "daily_calories": round(target_calories),
            "bmr": round(bmr),
            "nutrition_advice": advice,
            "meal_timing": "3 ana öğün + 2 ara öğün",
            "status": "success"
        }

    except Exception as e:
        return {"error": f"Beslenme önerisi hatası: {str(e)}"}

def get_exercise_plan(bmi: float, gender: str, age: int, fitness_goal: str = "auto") -> dict:
    """
    BMI ve hedeflere göre egzersiz planı önerir.

    Args:
        bmi: BMI değeri
        gender: Cinsiyet
        age: Yaş
        fitness_goal: Fitness hedefi ("kilo_verme", "kas_yapma", "form_koruma", "auto")

    Returns:
        Kişiselleştirilmiş egzersiz planı
    """
    try:
        # BMI'ye göre otomatik hedef belirleme
        if fitness_goal == "auto":
            if bmi < 18.5:
                fitness_goal = "kas_yapma"
            elif bmi >= 25:
                fitness_goal = "kilo_verme"
            else:
                fitness_goal = "form_koruma"

        # Yaşa göre yoğunluk ayarlama
        if age < 30:
            intensity = "yüksek"
        elif age < 50:
            intensity = "orta"
        else:
            intensity = "düşük"

        exercise_plans = {
            "kilo_verme": {
                "primary_focus": "Kalori yakma ve yağ kaybı",
                "cardio_percentage": 60,
                "strength_percentage": 40,
                "recommended_exercises": [
                    "🏃‍♂️ HIIT (Yüksek Yoğunluklu Interval Antrenman)",
                    "🚴‍♂️ Kardiyo (koşu, bisiklet, yüzme)",
                    "🏋️‍♂️ Compound hareketler (squat, deadlift)",
                    "🤸‍♂️ Fonksiyonel antrenmanlar",
                    "🧘‍♂️ Yoga veya Pilates"
                ],
                "weekly_frequency": "5-6 gün",
                "session_duration": "45-60 dakika",
                "tips": [
                    "💡 Kalori açığı oluşturun",
                    "💡 Kardiyo sonrası protein alın",
                    "💡 Antrenman öncesi hafif atıştırın"
                ]
            },
            "kas_yapma": {
                "primary_focus": "Kas kütlesi artırma",
                "cardio_percentage": 20,
                "strength_percentage": 80,
                "recommended_exercises": [
                    "🏋️‍♂️ Ağırlık antrenmanı (compound hareketler)",
                    "💪 İzolasyon egzersizleri",
                    "🤸‍♂️ Bodyweight egzersizleri",
                    "🏃‍♂️ Hafif kardiyo (ısınma için)",
                    "🧘‍♂️ Esneklik çalışmaları"
                ],
                "weekly_frequency": "4-5 gün",
                "session_duration": "60-90 dakika",
                "tips": [
                    "💡 Kalori fazlası oluşturun",
                    "💡 Antrenman sonrası protein alın",
                    "💡 Dinlenme günlerini ihmal etmeyin"
                ]
            },
            "form_koruma": {
                "primary_focus": "Genel fitness ve sağlık",
                "cardio_percentage": 50,
                "strength_percentage": 50,
                "recommended_exercises": [
                    "🏃‍♂️ Orta yoğunlukta kardiyo",
                    "🏋️‍♂️ Ağırlık antrenmanı",
                    "🧘‍♂️ Yoga veya Pilates",
                    "🚶‍♂️ Yürüyüş veya hafif koşu",
                    "🤸‍♂️ Fonksiyonel hareketler"
                ],
                "weekly_frequency": "4-5 gün",
                "session_duration": "45-60 dakika",
                "tips": [
                    "💡 Dengeli beslenin",
                    "💡 Çeşitlilik sağlayın",
                    "💡 Düzenli olun"
                ]
            }
        }

        plan = exercise_plans.get(fitness_goal, exercise_plans["form_koruma"])

        return {
            "fitness_goal": fitness_goal,
            "intensity_level": intensity,
            "plan": plan,
            "age_group": "genç" if age < 30 else "orta_yaş" if age < 50 else "yaşlı",
            "status": "success"
        }

    except Exception as e:
        return {"error": f"Egzersiz planı hatası: {str(e)}"}

def get_weekly_schedule(fitness_goal: str = "form_koruma", intensity: str = "orta") -> dict:
    """
    Haftalık detaylı antrenman programı oluşturur.

    Args:
        fitness_goal: Fitness hedefi
        intensity: Yoğunluk seviyesi

    Returns:
        7 günlük detaylı antrenman programı
    """
    try:
        schedules = {
            "kilo_verme": {
                "Pazartesi": {
                    "focus": "HIIT + Üst Vücut",
                    "exercises": [
                        "🔥 20 dk HIIT kardiyo",
                        "💪 Push-up 3x12",
                        "🏋️‍♂️ Dumbbell press 3x10",
                        "🤸‍♂️ Plank 3x30sn"
                    ],
                    "duration": "45 dakika"
                },
                "Salı": {
                    "focus": "Kardiyo + Alt Vücut",
                    "exercises": [
                        "🏃‍♂️ 30 dk koşu/bisiklet",
                        "🦵 Squat 3x15",
                        "🦵 Lunges 3x12",
                        "🧘‍♂️ Stretching 10 dk"
                    ],
                    "duration": "50 dakika"
                },
                "Çarşamba": {
                    "focus": "Aktif Dinlenme",
                    "exercises": [
                        "🚶‍♂️ 30 dk yürüyüş",
                        "🧘‍♂️ Yoga 20 dk",
                        "💧 Bol su tüketimi"
                    ],
                    "duration": "30 dakika"
                },
                "Perşembe": {
                    "focus": "Full Body HIIT",
                    "exercises": [
                        "🔥 25 dk HIIT",
                        "🏋️‍♂️ Burpees 3x8",
                        "🤸‍♂️ Mountain climbers 3x20",
                        "💪 Kettlebell swings 3x15"
                    ],
                    "duration": "45 dakika"
                },
                "Cuma": {
                    "focus": "Kardiyo + Core",
                    "exercises": [
                        "🏃‍♂️ 35 dk kardiyo",
                        "🤸‍♂️ Plank variations 3x30sn",
                        "💪 Russian twists 3x20",
                        "🧘‍♂️ Cool down 10 dk"
                    ],
                    "duration": "55 dakika"
                },
                "Cumartesi": {
                    "focus": "Outdoor Activity",
                    "exercises": [
                        "🚴‍♂️ Bisiklet 60 dk",
                        "🏊‍♂️ Yüzme (varsa)",
                        "🥾 Doğa yürüyüşü"
                    ],
                    "duration": "60+ dakika"
                },
                "Pazar": {
                    "focus": "Dinlenme",
                    "exercises": [
                        "🧘‍♂️ Hafif yoga",
                        "🚶‍♂️ Rahat yürüyüş",
                        "💤 Kaliteli uyku"
                    ],
                    "duration": "30 dakika"
                }
            },
            "kas_yapma": {
                "Pazartesi": {
                    "focus": "Göğüs + Triceps",
                    "exercises": [
                        "🏋️‍♂️ Bench press 4x8",
                        "💪 Dumbbell flyes 3x10",
                        "🤸‍♂️ Dips 3x12",
                        "💪 Tricep extensions 3x12"
                    ],
                    "duration": "75 dakika"
                },
                "Salı": {
                    "focus": "Sırt + Biceps",
                    "exercises": [
                        "🏋️‍♂️ Pull-ups 4x8",
                        "🏋️‍♂️ Rows 4x10",
                        "💪 Bicep curls 3x12",
                        "💪 Hammer curls 3x10"
                    ],
                    "duration": "75 dakika"
                },
                "Çarşamba": {
                    "focus": "Dinlenme",
                    "exercises": [
                        "🧘‍♂️ Hafif stretching",
                        "🚶‍♂️ 20 dk yürüyüş",
                        "💤 Kaliteli uyku"
                    ],
                    "duration": "30 dakika"
                },
                "Perşembe": {
                    "focus": "Bacak + Glutes",
                    "exercises": [
                        "🦵 Squats 4x10",
                        "🦵 Deadlifts 4x8",
                        "🦵 Leg press 3x12",
                        "🦵 Calf raises 3x15"
                    ],
                    "duration": "80 dakika"
                },
                "Cuma": {
                    "focus": "Omuz + Core",
                    "exercises": [
                        "🏋️‍♂️ Shoulder press 4x10",
                        "💪 Lateral raises 3x12",
                        "🤸‍♂️ Plank 3x45sn",
                        "💪 Russian twists 3x20"
                    ],
                    "duration": "70 dakika"
                },
                "Cumartesi": {
                    "focus": "Full Body",
                    "exercises": [
                        "🏋️‍♂️ Compound movements",
                        "🤸‍♂️ Functional training",
                        "🧘‍♂️ Mobility work"
                    ],
                    "duration": "60 dakika"
                },
                "Pazar": {
                    "focus": "Aktif Dinlenme",
                    "exercises": [
                        "🚶‍♂️ Hafif yürüyüş",
                        "🧘‍♂️ Yoga",
                        "💤 Dinlenme"
                    ],
                    "duration": "30 dakika"
                }
            }
        }

        # Form koruma için dengeli program
        if fitness_goal not in schedules:
            fitness_goal = "form_koruma"
            schedules["form_koruma"] = {
                "Pazartesi": {
                    "focus": "Kardiyo + Üst Vücut",
                    "exercises": [
                        "🏃‍♂️ 25 dk orta tempoda koşu",
                        "💪 Push-ups 3x10",
                        "🏋️‍♂️ Dumbbell rows 3x10"
                    ],
                    "duration": "45 dakika"
                },
                "Salı": {
                    "focus": "Strength + Alt Vücut",
                    "exercises": [
                        "🦵 Squats 3x12",
                        "🦵 Lunges 3x10",
                        "🧘‍♂️ Stretching 15 dk"
                    ],
                    "duration": "40 dakika"
                },
                "Çarşamba": {
                    "focus": "Yoga/Pilates",
                    "exercises": [
                        "🧘‍♂️ 45 dk yoga",
                        "🤸‍♂️ Core strengthening"
                    ],
                    "duration": "45 dakika"
                },
                "Perşembe": {
                    "focus": "Kardiyo",
                    "exercises": [
                        "🚴‍♂️ 30 dk bisiklet",
                        "🤸‍♂️ Plank 3x30sn"
                    ],
                    "duration": "40 dakika"
                },
                "Cuma": {
                    "focus": "Full Body",
                    "exercises": [
                        "🏋️‍♂️ Compound exercises",
                        "🤸‍♂️ Functional movements"
                    ],
                    "duration": "50 dakika"
                },
                "Cumartesi": {
                    "focus": "Outdoor/Fun",
                    "exercises": [
                        "🚶‍♂️ Doğa yürüyüşü",
                        "🏊‍♂️ Yüzme (varsa)"
                    ],
                    "duration": "60 dakika"
                },
                "Pazar": {
                    "focus": "Dinlenme",
                    "exercises": [
                        "🧘‍♂️ Hafif stretching",
                        "💤 Kaliteli uyku"
                    ],
                    "duration": "30 dakika"
                }
            }

        return {
            "fitness_goal": fitness_goal,
            "intensity": intensity,
            "weekly_schedule": schedules[fitness_goal],
            "total_weekly_hours": "5-7 saat",
            "rest_days": 1 if fitness_goal == "kas_yapma" else 2,
            "status": "success"
        }

    except Exception as e:
        return {"error": f"Haftalık program hatası: {str(e)}"}
