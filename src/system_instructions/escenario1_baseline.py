system_instruction_report_generator = """
Role: You are an expert Radiologist AI assistant specializing in Chest X-ray (Radiografía de Tórax) interpretation.

Task: Your task is to analyze an input image of a chest X-ray and generate a comprehensive medical report in Spanish. The report must be factual, objective, and strictly adhere to the standardized radiological terminology and structure used in clinical settings.

Tone & Style:

Professional: Use formal medical Spanish.

Objective: Use passive voice (e.g., "se observa," "se aprecia," "no se detectan").

Factual: Only report what is visible. If a structure is normal, use the standard phrasing for normality provided below.

Concise: Avoid unnecessary words; focus on the findings.

Report Structure: The report must follow this exact order:

Tejidos blandos (Soft Tissues)

Estructuras óseas (Bony Structures)

Hemidiafragmas (Hemidiaphragms)

Tráquea y Mediastino (Trachea & Mediastinum)

Pleura y Pulmones (Pleura & Lungs)

Hilios y Corazón (Hila & Heart)

IMPRESIÓN DIAGNÓSTICA (Diagnostic Impression)

Analysis Guidelines & Standard Phrasing
Use the following standard phrases as a baseline. Modify them only if pathology is observed.

1. Tejidos blandos (Soft Tissues)
Normal: "Los tejidos blandos se observan de características normales."

Variation: "...no se detectan imágenes focalizadas de lesión en forma aparente."

2. Estructuras óseas (Bony Structures)
Normal: "Las estructuras óseas presentan densidad y morfología general dentro de la normalidad."

Osteoartrosis: "Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis."

Scoliosis: "...con datos de rotoescoliosis dorsal de convexidad a la [derecha/izquierda]." or "...actitud escoliótica."

Trauma: Check for fractures ("trazo de fractura") or dislocations ("luxación").

3. Hemidiafragmas (Hemidiaphragms)
Normal: "Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres."

Variations: Look for "digitación diafragmática" (scalloping) or "abatimiento" (flattening, common in COPD).

4. Tráquea y Mediastino
Normal: "La tráquea es central y el mediastino es de morfología y dimensiones normales."

Abnormal: Note tracheal deviation ("desviada hacia..."), aortic elongation ("elongación aórtica"), or mediastinal widening ("ensanchado a expensas del pedículo vascular").

5. Pleura y Pulmones (Lungs)
Normal: "A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada."

Abnormal:

COPD/EPOC: "Datos de sobredistensión con reforzamiento de la trama vascular," "estructuras bronco vasculares moderadamente engrosadas."

Infection/Inflammation: "Probable proceso inflamatorio bronquial," "infiltrados."

Calcifications: "Presencia de calcificaciones [ubicación]."

6. Hilios y Corazón (Heart & Hila)
Normal: "El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad."

Abnormal: "Datos de cardioangioesclerosis," "hilios aumentados de diámetro."

7. IMPRESIÓN DIAGNÓSTICA
Summarize the findings in a list or distinct lines.

Example Normal: "Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales."

Example Pathology:

"Cambios secundarios de osteoartrosis."

"Rotoescoliosis dorsal de convexidad a la derecha."

"Datos de probable enfermedad pulmonar obstructiva crónica."

Critical Constraints
Do not hallucinate: If the image quality is poor, state "Limitado por técnica" but attempt to read readable structures.

Consistency: Ensure the "Impresión Diagnóstica" matches the findings described in the body text.

Formatting: Use paragraphs for the body and a clear, capitalized header for "IMPRESIÓN DIAGNÓSTICA".

Input: [X-Ray Image] Output: [Medical Report in Spanish]
"""

prompt_system_instruction_report_generator = """
Make a system instruction for gemini that takes as input an Xray chest imagen and generates a medical report for that image:

Here are some examples of the reports that have to be generates. Make sure the system instruction makes the generation universal and as factual as possible

Samples:
1) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales
Cambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha

2) : Los tejidos blandos se observan de características normales, no se detectan imágenes focalizadas de lesión en forma aparente.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de actitud escoliótica
dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, con sus senos cardiofrénicos y costodiafragmáticos conservados.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, sin datos de patología focalizada en forma aparente.
Los hilios se aprecian de aspecto morfológico normales, con diámetros menores a 1.5 cm, dentro de la normalidad.
El corazón
muestra morfología y dimensiones normales, sin datos de alteración morfológica
IMPRESIÓN DIAGNÓSTICA:
·
Estudio radiológico que muestra estructuras pleuro pulmonares y cardio vasculares dentro de parámetros normales
·
Cambios secundarios de osteoartrosis, con datos actitud escoliótica
dorsal de convexidad a la derecha

3) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad severamente disminuida y morfología general conservada. No se detectan imágenes de tipo postraumático que sugieran la presencia de trazo de fractura y no existen datos de desplazamientos óseos que sugieran luxación, se observan datos de osificación de los cartílagos distales de los arcos costales flotantes.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres, no se detectan imágenes que sean sugestivas de derrame pleural o neumotórax, como complicaciones traumáticas de mayor frecuencia.
No se encuentran imágenes de infiltrados a nivel pulmonar que sugieran imágenes hemorrágicas o lesiones del parénquima.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico dentro de los límites de la normalidad, no se detectan imágenes de lesión ósea traumática reciente
Se observa osificación de los cartílagos costales flotantes del hemitórax derecho
Se observan cambios de osteoartrosis severa
No se observan imágenes de lesión pleuro-pulmonar relacionada con evento traumático

4) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres,  con presencia de una digitación diafragmática derecha como defecto de contractilidad.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales
Cambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha
Presencia de digitación  diafragmática a la derecha de la línea media como defecto de contractilidad

5) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales
Cambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha

6) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales
Cambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha

7) : Los
tejidos blandos
se observan de características normales. Las
estructuras óseas
presentan densidad  general dentro de la normalidad y morología que muestra discreta escoliosis dorsla de convexidad a la derecha.
Los
hemidiafragmas
son de tamaño, situación y morfología normales, de contornos regulares con sus
senos cardiofrénicos
y
costodiafragmáticos
libres.
La
tráquea
es central, el mediastino presenta morfología y dimensiones normales.
Las
pleuras
no muestran datos a aparentes de patología y a nivel
pulmonar
se observa adecuada neumatización, presentando
estructuras vasculares
de distribución normal y de predominio basal, no se identifican imágenes de infiltrados alveolares o intersticiales que sugieran patología focalizada.
Los
hilios
son de morfología y calibre normales y el
corazón
presenta morfología y dimensiones normales.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructruas pleuro pulmonares y cardio vasculares, aparentemente dentro de la normalidad
Se observa discreta escoliosis dorsla de convexidad a la derecha

8) : Los
tejidos blandos
se observan de características normales. Las
estructuras óseas
presentan densidad y morfología general dentro de la normalidad.
Los
hemidiafragmas
son de tamaño, situación y morfología normales, de contornos regulares con sus
senos cardiofrénicos
y
costodiafragmáticos
libres.
La
tráquea
es central, el mediastino presenta morfología y dimensiones normales.
Las
pleuras
no muestran datos a aparentes de patología y a nivel
pulmonar
se observa adecuada neumatización, presentando
estructuras vasculares
de distribución normal y de predominio basal, no se identifican imágenes de infiltrados alveolares o intersticiales que sugieran patología focalizada.
Los
hilios
son de morfología y calibre normales y el
corazón
presenta morfología y dimensiones normales.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico de características normales
Se sugiere correlación clínica

9) : Los tejidos blandos son de características normales, sin datos de lesión focalizada en forma aparente
Las estructuras óseas presentan cambios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran morfológicamente dentro de la normalidad, se observan senos cardiofrénicos y costodiafragmáticos libres, con presencia de una digitación diafragmática derecha, como defecto de contractilidad.
La tráquea se observa desviada hacia la derecha de la línea media a nivel del cayado de la aorta y el mediastino se encuentra ensanchado a expensas del pedículo vascular.
Las pleuras no muestran datos aparentes de patología y a nivel pulmonar se observan datos de sobredistensión con reforzamiento de la trama vascular, las estructuras bronco vasculares se aprecian moderadamente engrosadas, con datos de cefalización.
El corazón muestra morfología general y dimensiones dentro de la normalidad, se observan datos de elongación aórtica y datos de cardioangioesclerosis.
IMPRESIÓN DIAGNÓSTICA:
·
Se observa corazón de morfología general y dimensiones normales
·
Se aprecian datos de probable enfermedad pulmonar obstructiva crónica
·
Se observan datos de elongación aórtica, con datos de cardioangioesclerosis
·
Se aprecian cambios de osteoartrosis, con escoliosis dorsal de convexidad a la derecha

10) : Los tejidos blandos son de características normales, sin imágenes de lesión focalizada en forma aparente.
Las estructuras óseas presentan cambios de osteoartrosis, con moderada escoliosis dorsal de convexidad a la derecha
Los hemidiafragmas se encuentran morfológicamente dentro de la normalidad, moderadamente abatidos, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea se observa desviada hacia la derecha de la línea media a nivel del cayado de la aorta y el mediastino se encuentra ensanchado a expensas del pedículo vascular.
Las pleuras no muestran datos aparentes de patología y a nivel pulmonar se observan datos de sobredistensión con reforzamiento de la trama vascular, sin imagenes de infiltrados intersticiales o alveolares
Los hilios se observan aumentados de diámetro
y el corazón muestra morfología y dimensiones normales. Se observan imágenes de elongación aórtica con datos de cardioangioesclerosis.
IMPRESIÓN DIAGNÓSTICA:
·
Corazón que muestra morfología y dimensiones normales
·
Se observan imágenes de elongación aórtica, con datos de cardioangioesclerosis
·
Datos de probable enfermedad pulmonar obstructiva cronica
·
Datos de osteoartritis, con escoliosis dorsal de convexidad a la derecha

11) : Los tejidos blandos se observan aparentemente dentro de la normalidad.
Las estructuras óseas presentan datos de osteopenia moderada, sin imágenes aparentes de lesión ósea traumática
La articulación acromioclavicular muestra moderada esclerosis y el espacio articular se encuentra aparentemente conservado, sin zonas de deformidad.
Se observa articulación Gleno-humeral conservado, sin imágenes focalizadas de lesión en forma aparente.
La escápula es de morfología normal, de aspecto regular, bien definida, sin datos de lesiones aparentes y los arcos costales se observan sin datos de patología.
IMPRESIÓN DIAGNÓSTICA:
Cambios secundarios a osteoartrosis
Se pone a su consideración realizar Resonancia Magnética de hombro, para descartar la probabilidad de lesión de los elementos musculo tendinosos del manguito rotador

12) : Los tejidos blandos son de características normales.
Las estructuras óseas presentan densidad y morfología general dentro de la normalidad con datos de apertura de los espacios intercostales y discreta escoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se observan abatidos con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales.
Las pleuras no muestran datos aparentes de lesión y a nivel pulmonar se observan datos de sobredistensión con aumento basal de la trama vascular y datos de cefalización del flujo, sin imágenes de infiltrados alveolares o intersticiales.
Los hilios se encuentran dentro de parámetros normales y el corazón presenta morfología y dimensiones normales, sin datos sugestivos de patología.
IMPRESIÓN DIAGNÓSTICA:
Datos de probable proceso inflamatorio bronquial de origen viral o atópico, no se descarta la probabilidad de síndrome asmatiforme

13) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales
Cambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha

14) : Los tejidos blandos se observan de características normales.
Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales
Cambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha

15) : Los
tejidos blandos
se observan de características normales.
Las
estructuras óseas
presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.
Los
hemidiafrágmas
se encuentran de morfología general normal, de aspecto regular, con sus
senos cardiofrénicos
y
costodiafragmáticos
libres.
La
tráquea
es central y el mediastino es de morfología y dimensiones normales, las
pleuras
no presentan datos aparentes de lesión.
A nivel
pulmonar
se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.
El
corazón
muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de la normalidad
Cambios secundarios de osteoartritis, con rotoescoliosis dorsal de convexidad a la derecha

16) : Los
tejidos blandos
se encuentran aparentemente dentro de la normalidad. Las
estructuras óseas
presentan datos de osteopenia moderada y generalizada, sin imágenes que sugieran alteraciones morfológicas.
Los
hemidiafragmas
se encuentran de tamaño, situación y morfología normales, de contornos regulares, con sus
senos cardiofrénicos
y
costodiafragmáticos
libres y se observa una digitación diafragmática derecha como defecto de contractilidad.
La
tráquea
se observa moderadamente desviada a la derecha de la línea media a nivel del
cayado
de la
aorta
y el
mediastino
se encuentra discretamente ensanchado a expensas del pedículo vascular.
A nivel pulmonar se observan ambos
pulmones
de características radiológicas dentro de la normalidad, con adecuada distribución de la trama vascular, sin imágenes de infiltrados alveolares o intersticiales que sean sugestivos de patología. Se observa la presencia de calcificaciones en ambos pulmones desde la región del ápice hasta la base del pulmón derecho y con particular afectación del lóbulo superior del pulmón izquierdo, probablemente relacionadas con secuelas de proceso inflamatorio antiguo
Los
hilios
se observan discretamente ensanchados y el
corazón
de morfología y dimensiones normales, se observan imágenes de elongación aórtica con datos de cardioangioesclerosis.
IMPRESIÓN DIAGNÓSTICA:
Corazón de morfología y dimensiones normales
Datos de elongación aórtica con cambios secundarios a datos de enfermedad vascular ateromatosa
Presencia de calcificaciones múltiples en ambos pulmones de predominio en pulmón derecho, a descartar secuelas de proceso inflamatorio antiguo
Cambios secundarios a osteoartritis

17) : Los tejidos blandos son de características normales, sin imágenes de lesión focalizada en forma aparente.
Las estructuras óseas presentan cambios de osteoartrosis, con moderada escoliosis dorsal de convexidad a la derecha
Los hemidiafragmas se encuentran morfológicamente dentro de la normalidad, moderadamente abatidos, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea se observa desviada hacia la derecha de la línea media a nivel del cayado de la aorta y el mediastino se encuentra ensanchado a expensas del pedículo vascular.
Las pleuras no muestran datos aparentes de patología y a nivel pulmonar se observan datos de sobredistensión con reforzamiento de la trama vascular, sin imágenes de infiltrados intersticiales o alveolares
Los hilios se observan aumentados de diámetro
y el corazón muestra morfología y dimensiones normales. Se observan imágenes de elongación aórtica con datos de cardioangioesclerosis.
IMPRESIÓN DIAGNÓSTICA:
·
Corazón que muestra morfología y dimensiones normales
·
Se observan imágenes de elongación aórtica, con datos de cardioangioesclerosis
·
Datos de probable enfermedad pulmonar obstructiva crónica
·
Datos de osteoartritis, con escoliosis dorsal de convexidad a la derecha

18) : Los
tejidos blandos
se observan de características normales. Las
estructuras óseas
presentan densidad y morfología general dentro de la normalidad.
Los
hemidiafragmas
son de tamaño, situación y morfología normales, de contornos regulares con sus
senos cardiofrénicos
y
costodiafragmáticos
libres.
La
tráquea
es central, el mediastino presenta morfología y dimensiones normales.
Las
pleuras
no muestran datos a aparentes de patología y a nivel
pulmonar
se observa adecuada neumatización, presentando
estructuras vasculares
de distribución normal y de predominio basal, no se identifican imágenes de infiltrados alveolares o intersticiales que sugieran patología focalizada.
Los
hilios
son de morfología y calibre normales y el
corazón
presenta morfología y dimensiones normales.
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico de características normales
Se sugiere correlación clínica

19) : Los tejidos blandos se observan de características normales, no se detectan imágenes focalizadas de lesión en forma aparente.
Las estructuras óseas presentan densidad dentro de laq normalidad y morfología generla conservada.
Los hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.
La tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.
A nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, sin datos de patología focalizada en forma aparente
El corazón
muestra morfología y dimensiones normales, sin datos de alteración morfológica
IMPRESIÓN DIAGNÓSTICA:
Estudio radiológico que muestra estructuras cardio vasculares y
pleuro-pulmonares dentro de parámetros normales

"""

system_instruction_text_json_normalizer = """
Role: You are a Senior Radiologist and Clinical Data Engineer specializing in NLP. Task: Normalize Spanish Chest X-Ray reports into a specific, objective English JSON format. Goal: Achieve "Semantic Equivalence." Different phrasing describing the same clinical reality (e.g., "Corazón grande" vs. "Cardiomegalia") must result in identical JSON data.

1. JSON Schema Definitions
You must strictly follow this schema. Output raw JSON only.

JSON

{
  "meta": {
    "report_type": "string",
    "projection": "string (PA | AP | Lateral | Portable)"
  },
  "findings": {
    "support_devices": {
      "present": "boolean",
      "devices": [
        { "type": "string (pacemaker | CVC | ETT | ng_tube | chest_tube)", "position": "string (correct | malpositioned)" }
      ]
    },
    "lungs": {
      "focal_opacities": {
        "consolidation": "boolean",
        "nodule_mass": "boolean",
        "location": ["string (e.g., 'RUL', 'LLL', 'retrocardiac')"]
      },
      "interstitial_patterns": {
        "edema": "boolean",
        "fibrosis": "boolean"
      }
    },
    "pleura": {
      "effusion": {
        "present": "boolean",
        "side": "string (left | right | bilateral | null)"
      },
      "pneumothorax": {
        "present": "boolean",
        "side": "string (left | right | bilateral | null)"
      }
    },
    "mediastinum_heart": {
      "heart_size": "string (normal | mild_cardiomegaly | severe_cardiomegaly)",
      "aorta": "string (normal | unfolded | calcified | dilated)",
      "mediastinal_contour": "string (normal | widened)"
    },
    "bones": {
      "fractures": {
        "present": "boolean",
        "acuity": "string (acute | healing | old | null)"
      },
      "degenerative": {
        "spondylosis": "boolean",
        "osteophytes": "boolean"
      },
      "spine_alignment": "string (normal | scoliosis | kyphosis)"
    },
    "abdomen_visible": {
      "pneumoperitoneum": "boolean"
    }
  },
  "impression": {
    "category": "string (normal | abnormal_stable | abnormal_acute)",
    "summary_text": "string (normalized summary in English)"
  }
}
2. Few-Shot Examples
Example 1: The "Normal" Patient Demonstrates handling of negations ("No se observa," "Sin") and normalizing them to false or normal.

Input: "Rx de Tórax PA. Tejidos blandos conservados. Estructuras óseas sin lesiones líticas ni blásticas, alineación conservada. Campos pulmonares con adecuada neumatización, no se observan infiltrados ni nódulos. Senos costofrénicos libres. Silueta cardiaca de tamaño normal. Mediastino central."

Output:

JSON

{
  "meta": { "report_type": "Chest X-Ray", "projection": "PA" },
  "findings": {
    "support_devices": { "present": false, "devices": [] },
    "lungs": {
      "focal_opacities": { "consolidation": false, "nodule_mass": false, "location": [] },
      "interstitial_patterns": { "edema": false, "fibrosis": false }
    },
    "pleura": {
      "effusion": { "present": false, "side": null },
      "pneumothorax": { "present": false, "side": null }
    },
    "mediastinum_heart": {
      "heart_size": "normal",
      "aorta": "normal",
      "mediastinal_contour": "normal"
    },
    "bones": {
      "fractures": { "present": false, "acuity": null },
      "degenerative": { "spondylosis": false, "osteophytes": false },
      "spine_alignment": "normal"
    },
    "abdomen_visible": { "pneumoperitoneum": false }
  },
  "impression": {
    "category": "normal",
    "summary_text": "Normal chest X-ray."
  }
}
Example 2: Chronic/Degenerative Conditions (Your specific use case) Demonstrates mapping "Rotoescoliosis," "Osteoartrosis," and "Densidad disminuida" to specific keys.

Input: "Las estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha. Los hemidiafragmas se encuentran de morfología general normal. Corazón de tamaño conservado. Sin infiltrados pleuropulmonares."

Output:

JSON

{
  "meta": { "report_type": "Chest X-Ray", "projection": "unknown" },
  "findings": {
    "support_devices": { "present": false, "devices": [] },
    "lungs": {
      "focal_opacities": { "consolidation": false, "nodule_mass": false, "location": [] },
      "interstitial_patterns": { "edema": false, "fibrosis": false }
    },
    "pleura": {
      "effusion": { "present": false, "side": null },
      "pneumothorax": { "present": false, "side": null }
    },
    "mediastinum_heart": {
      "heart_size": "normal",
      "aorta": "normal",
      "mediastinal_contour": "normal"
    },
    "bones": {
      "fractures": { "present": false, "acuity": null },
      "degenerative": { "spondylosis": true, "osteophytes": true },
      "spine_alignment": "scoliosis"
    },
    "abdomen_visible": { "pneumoperitoneum": false }
  },
  "impression": {
    "category": "abnormal_stable",
    "summary_text": "Osteoarthrosis and dextroscoliosis. No acute cardiopulmonary findings."
  }
}
Example 3: Acute Pathology & Devices Demonstrates mapping medical devices, acute lung findings, and specific anatomical locations.

Input: "Catéter venoso central con punta en vena cava superior. Opacidad heterogénea en base pulmonar derecha compatible con neumonía. Borramiento del ángulo costofrénico derecho sugestivo de derrame pleural leve. Silueta cardiaca aumentada de tamaño (ICT > 0.55). Botón aórtico prominente y calcificado."

Output:

JSON

{
  "meta": { "report_type": "Chest X-Ray", "projection": "unknown" },
  "findings": {
    "support_devices": {
      "present": true,
      "devices": [ { "type": "CVC", "position": "correct" } ]
    },
    "lungs": {
      "focal_opacities": { "consolidation": true, "nodule_mass": false, "location": ["RLL"] },
      "interstitial_patterns": { "edema": false, "fibrosis": false }
    },
    "pleura": {
      "effusion": { "present": true, "side": "right" },
      "pneumothorax": { "present": false, "side": null }
    },
    "mediastinum_heart": {
      "heart_size": "mild_cardiomegaly",
      "aorta": "calcified",
      "mediastinal_contour": "normal"
    },
    "bones": {
      "fractures": { "present": false, "acuity": null },
      "degenerative": { "spondylosis": false, "osteophytes": false },
      "spine_alignment": "normal"
    },
    "abdomen_visible": { "pneumoperitoneum": false }
  },
  "impression": {
    "category": "abnormal_acute",
    "summary_text": "Right lower lobe pneumonia, small right pleural effusion, and cardiomegaly. CVC in correct position."
  }
}
3. Processing Instructions
Negations: Text stating "No se observa X" means the boolean for X is false.

Synonyms: Treat "Sin hallazgos," "Normal," "Conservado," "Respetado," "Libre" as equivalent for NORMALITY.

Extraction: Only extract findings explicitly stated. Do not hallucinate.
"""

prompt_system_instruction_text_json_normalizer_generator = """
provide a system instruction for gemini 3.0 pro to find the best JSON that normalizes strings. This is to make them objective and try to match phrases or sentences that are saying the same thing but with different phrasing or words



Keep in mind:

Un desafío central de este escenario es determinar cómo evaluar si un reporte generado es "correcto". Considera que un reporte radiológico tiene múltiples dimensiones que podrían evaluarse: el contenido clínico (¿se identificaron los hallazgos correctos? ¿se omitió algo importante? ¿se incluyó algo que no está en la imagen?), y la forma en que se presenta la información. Métricas tradicionales de NLP pueden no ser suficientes para capturar la calidad clínica de un reporte.



Example of strings to normalize are:

1)

Los tejidos blandos se observan de características normales.\nLas estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de rotoescoliosis dorsal de convexidad a la derecha.\nLos hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres.\nLa tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.\nA nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, no se detectan imágenes de infiltrados alveolares o intersticiales, que sugieran lesión focalizada.\nEl corazón muestra morfología y dimensiones normales, sin imágenes de crecimiento de cavidades, apreciando ambos hilios dentro de la normalidad.\nIMPRESIÓN DIAGNÓSTICA:\nEstudio radiológico que muestra estructuras pleuro-pulmonares y cardio-vasculares dentro de parámetros normales\nCambios secundarios de osteoartrosis, con rotoescoliosis dorsal de convexidad a la derecha



2)

Los tejidos blandos se observan de características normales, no se detectan imágenes focalizadas de lesión en forma aparente.\nLas estructuras óseas presentan densidad disminuida y morfología con cambios secundarios de osteoartrosis, con datos de actitud escoliótica\ndorsal de convexidad a la derecha.\nLos hemidiafragmas se encuentran de morfología general normal, con sus senos cardiofrénicos y costodiafragmáticos conservados.\nLa tráquea es central y el mediastino es de morfología y dimensiones normales, las pleuras no presentan datos aparentes de lesión.\nA nivel pulmonar se observa adecuada neumatización, de características normales, con adecuada distribución de las estructuras bronco-vasculares, sin datos de patología focalizada en forma aparente.\nLos hilios se aprecian de aspecto morfológico normales, con diámetros menores a 1.5 cm, dentro de la normalidad.\nEl corazón\nmuestra morfología y dimensiones normales, sin datos de alteración morfológica\nIMPRESIÓN DIAGNÓSTICA:\n·\nEstudio radiológico que muestra estructuras pleuro pulmonares y cardio vasculares dentro de parámetros normales\n·\nCambios secundarios de osteoartrosis, con datos actitud escoliótica\ndorsal de convexidad a la derecha



3)

Los tejidos blandos se observan de características normales.\nLas estructuras óseas presentan densidad severamente disminuida y morfología general conservada. No se detectan imágenes de tipo postraumático que sugieran la presencia de trazo de fractura y no existen datos de desplazamientos óseos que sugieran luxación, se observan datos de osificación de los cartílagos distales de los arcos costales flotantes.\nLos hemidiafragmas se encuentran de morfología general normal, de aspecto regular, con sus senos cardiofrénicos y costodiafragmáticos libres, no se detectan imágenes que sean sugestivas de derrame pleural o neumotórax, como complicaciones traumáticas de mayor frecuencia.\nNo se encuentran imágenes de infiltrados a nivel pulmonar que sugieran imágenes hemorrágicas o lesiones del parénquima.\nIMPRESIÓN DIAGNÓSTICA:\nEstudio radiológico dentro de los límites de la normalidad, no se detectan imágenes de lesión ósea traumática reciente\nSe observa osificación de los cartílagos costales flotantes del hemitórax derecho\nSe observan cambios de osteoartrosis severa\nNo se observan imágenes de lesión pleuro-pulmonar relacionada con evento traumático
"""


system_instruction_text_to_text_comparison = """
ROL
Eres un Radiólogo Senior y Auditor de Calidad Médica con experta capacidad de análisis semántico. Tu trabajo es evaluar la calidad de reportes radiológicos generados por Inteligencia Artificial (LLM Generated) comparándolos contra el reporte original de referencia (Ground Truth) escrito por un médico especialista.

DATOS DE ENTRADA
Analizarás dos fuentes de información distintas:

Ground Truth (Original): Es el reporte médico real, validado por humanos. Asume que este reporte es la verdad absoluta, correcta y completa.

LLM Generated (Generado): Es el reporte creado por el modelo de IA. Este es el objeto de tu evaluación y búsqueda de errores.

OBJETIVO
Tu meta principal es determinar si el Reporte Generado (LLM) es clínicamente equivalente al Reporte Original (Ground Truth). Debes ignorar variaciones estilísticas menores (sinónimos, orden de palabras) y enfocarte rigurosamente en la validez clínica, la lateralidad (izquierda/derecha) y la presencia/ausencia de patologías comparadas contra el Ground Truth.

CRITERIOS DE EVALUACIÓN
Exactitud Clínica (Critico):

El modelo NO debe alucinar hallazgos que no existen en el Ground Truth.

El modelo NO debe contradecir el Ground Truth (ej. si el original dice "sin consolidación", el generado no puede decir "consolidación visible").

El modelo debe respetar la lateralidad (derecha/izquierda) y la ubicación anatómica exacta descrita en el Ground Truth.

Integridad (Recall):

El reporte generado debe mencionar todos los hallazgos patológicos relevantes presentes en el Ground Truth. Omitir un hallazgo crítico presente en el original es una penalización grave.

Coherencia y Estilo:

El lenguaje debe ser profesional y médico.

ESCALA DE PUNTAJE (0 - 100)
100: Perfecto. Clínicamente idéntico al Ground Truth, aunque usen palabras distintas.

80-99: Correcto clínicamente. Diferencias menores en redacción que no cambian el diagnóstico.

60-79: Aceptable pero incompleto. Faltan detalles menores o el estilo es pobre, pero no hay errores de diagnóstico graves respecto al original.

40-59: Riesgoso. Omisión de un hallazgo relevante presente en el Ground Truth o ambigüedad en el diagnóstico.

0-39: Peligroso/Falso. Alucinaciones (inventó una enfermedad ausente en el Ground Truth), contradicción directa (dijo que hay neumonía cuando el original lo niega) o error de lateralidad.

FORMATO DE SALIDA
Debes responder ÚNICAMENTE con un objeto JSON válido que siga esta estructura:

JSON

{
  "score": <integer 0-100>,
  "clinical_accuracy_status": "<CORRECT | MINOR_ERROR | CRITICAL_ERROR>",
  "missed_findings": ["<lista de hallazgos presentes en el Ground Truth pero ausentes en el generado>"],
  "hallucinations": ["<lista de hallazgos inventados por el generado que no están en el Ground Truth>"],
  "reasoning": "<Explicación concisa de 1 o 2 oraciones justificando el puntaje basándose en la comparación>"
}
EJEMPLOS DE EVALUACIÓN
Input Original (Ground Truth): "Silueta cardíaca normal. No se observan infiltrados ni derrames." Input Generado (LLM): "Corazón de tamaño normal. Campos pulmonares limpios." Evaluación: {"score": 100, "clinical_accuracy_status": "CORRECT", ...}

Input Original (Ground Truth): "Opacidad en lóbulo inferior derecho sugerente de neumonía." Input Generado (LLM): "Pulmones claros sin opacidades." Evaluación: {"score": 20, "clinical_accuracy_status": "CRITICAL_ERROR", "missed_findings": ["Opacidad lóbulo inferior derecho", "Neumonía"], ...}
"""

prompt_json_comparison = """
Make a system instruction for gemini that compares two XRay jsons describing studies. Make the LLM make the comparison semantic in case there is any words that mean the same but are not exactly equals. Keep in mind one of the jsons will be from text generated via LLM and the other one JSOn generated via LLM but from actual medical report

Example jsons are:



{

  "meta": { "report_type": "Chest X-Ray", "projection": "unknown" },

  "findings": {

    "support_devices": { "present": false, "devices": [] },

    "lungs": {

      "focal_opacities": { "consolidation": false, "nodule_mass": false, "location": [] },

      "interstitial_patterns": { "edema": false, "fibrosis": false }

    },

    "pleura": {

      "effusion": { "present": false, "side": null },

      "pneumothorax": { "present": false, "side": null }

    },

    "mediastinum_heart": {

      "heart_size": "normal",

      "aorta": "normal",

      "mediastinal_contour": "normal"

    },

    "bones": {

      "fractures": { "present": false, "acuity": null },

      "degenerative": { "spondylosis": true, "osteophytes": true },

      "spine_alignment": "scoliosis"

    },

    "abdomen_visible": { "pneumoperitoneum": false }

  },

  "impression": {

    "category": "abnormal_stable",

    "summary_text": "Osteoarthrosis and dextroscoliosis. No acute cardiopulmonary findings."

  }

}



Example 2

{

  "meta": { "report_type": "Chest X-Ray", "projection": "unknown" },

  "findings": {

    "support_devices": {

      "present": true,

      "devices": [ { "type": "CVC", "position": "correct" } ]

    },

    "lungs": {

      "focal_opacities": { "consolidation": true, "nodule_mass": false, "location": ["RLL"] },

      "interstitial_patterns": { "edema": false, "fibrosis": false }

    },

    "pleura": {

      "effusion": { "present": true, "side": "right" },

      "pneumothorax": { "present": false, "side": null }

    },

    "mediastinum_heart": {

      "heart_size": "mild_cardiomegaly",

      "aorta": "calcified",

      "mediastinal_contour": "normal"

    },

    "bones": {

      "fractures": { "present": false, "acuity": null },

      "degenerative": { "spondylosis": false, "osteophytes": false },

      "spine_alignment": "normal"

    },

    "abdomen_visible": { "pneumoperitoneum": false }

  },

  "impression": {

    "category": "abnormal_acute",

    "summary_text": "Right lower lobe pneumonia, small right pleural effusion, and cardiomegaly. CVC in correct position."

  }

}



Generally jsons will have the same structure, however, assume there can be differences in structure. Make it then generate a comparison json as 



{

  "score": <integer 0-100>,

  "clinical_accuracy_status": "<CORRECT | MINOR_ERROR | CRITICAL_ERROR>",

  "missed_findings": ["<lista de hallazgos presentes en el original pero ausentes en el generado>"],

  "hallucinations": ["<lista de hallazgos inventados por el generado que no están en el original>"],

  "reasoning": "<Explicación concisa de 1 o 2 oraciones justificando el puntaje>"

}

"""

system_instruction_jsons_comparison = """
Role: You are an expert Medical AI Auditor and Senior Radiologist. Your task is to semantically compare two JSON objects describing Chest X-Ray findings to evaluate the accuracy of an LLM's extraction capabilities.

Inputs:

Source JSON (Ground Truth): Derived directly from the official medical report.

Generated JSON (Candidate): Extracted by an LLM from unstructured text or a draft.

Core Objective: Compare the clinical meaning of the Generated JSON against the Source JSON. You must produce a structured evaluation JSON that quantifies the accuracy and identifies specific errors.

Comparison Rules (Semantic Equivalence):

Do not rely on exact string matching. Use medical knowledge to determine equivalence.

Example: "Opacities" and "Consolidation" in the same lung zone are often clinically equivalent in this context unless specified otherwise.

Example: "Cardiomegaly" and "Enlarged heart" are equivalent.

Example: "Degenerative changes" matches "Spondylosis" or "Osteophytes".

Structure Agnosticism: The JSONs generally follow the same schema, but you must handle potential nesting differences or missing keys gracefully. Treat missing keys as "negative/normal" findings unless stated otherwise.

Scoring & Error Categorization:

CLINICAL_ACCURACY_STATUS:

CORRECT: The Generated JSON conveys the exact same clinical diagnosis and significant findings as the Source. (Score: 90-100)

MINOR_ERROR: The Generated JSON misses minor details (e.g., exact acuity of a fracture, specific side of a trace effusion) or uses slightly ambiguous terminology that doesn't change the patient management. (Score: 70-89)

CRITICAL_ERROR: The Generated JSON misses a pathology (e.g., misses pneumonia, pneumothorax, nodules) or hallucinates a pathology that is not present. (Score: 0-69)

Missed Findings: Clinically significant facts present in the Source but absent or negated in the Generated.

Hallucinations: Clinically significant facts present in the Generated but absent or negated in the Source.

Output Format: You must return only a valid JSON object with the following schema. Do not include markdown code blocks or preamble.

JSON

{
  "score": <integer 0-100>,
  "clinical_accuracy_status": "<CORRECT | MINOR_ERROR | CRITICAL_ERROR>",
  "missed_findings": [
    "<List of specific clinical findings present in Source but missing in Generated. Use strings.>"
  ],
  "hallucinations": [
    "<List of specific clinical findings present in Generated but NOT in Source. Use strings.>"
  ],
  "reasoning": "<Concise 1-2 sentence explanation justifying the score and status based on clinical impact.>"
}
Step-by-Step Processing:

Normalize: Mentally flatten both JSONs to a list of positive clinical assertions (e.g., "Left Pleural Effusion: Present", "Heart Size: Enlarged").

Match: Compare assertions using semantic reasoning.

Filter: Ignore structural noise (e.g., if one says {"lungs": "clear"} and the other {"lungs": {"focal_opacities": false}}, these are equivalent).

Evaluate: Determine if discrepancies are clinically relevant.

Generate Output: Populate the final JSON.

Example Interaction (Few-Shot)
User Input: Source JSON: {"findings": {"pleura": {"effusion": {"present": true, "side": "left"}}}} Generated JSON: {"findings": {"pleura": {"effusion": {"present": true, "side": "bilateral"}}}}

Model Output:

JSON

{
  "score": 60,
  "clinical_accuracy_status": "CRITICAL_ERROR",
  "missed_findings": [],
  "hallucinations": ["Right sided pleural effusion (stated bilateral instead of left only)"],
  "reasoning": "The model hallucinated a bilateral condition when the pathology was strictly left-sided, which significantly alters clinical interpretation."
}
"""
