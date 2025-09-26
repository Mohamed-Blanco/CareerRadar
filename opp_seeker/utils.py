
import json
from datetime import datetime

from opp_seeker.logger import Logger
logger = Logger().get_logger()

class Utils :
    def __init__(self):
        pass

    def tuple_job_into_dictionary_skills(self,jobs):

        try:
            jobs_json = []

            for job in jobs :
                job = {
                    "original_job_id": job[0],
                    "location":job[1],
                    "sector_travail":job[2],
                    "entreprise":job[3],
                    "title":job[4],
                    "skills":job[5],
                    "months_of_experience": job[6],
                    "date_processement":job[7].strftime('%Y-%m-%d'),
                    "date_posted":job[8].strftime('%Y-%m-%d'),
                    "total_skills": job[9],
                    "matching_skills": job[10],
                    "job_details":job[11]
                }

                jobs_json.append(job)

            return jobs_json
        except Exception as e :
            logger.error(f"Error {e}")

    # def map_jobs(self,jobs):
    #     jobs_formatted = []
    #     if jobs:
    #         for job in jobs:
    #             job_formatted = {
    #                 "originalId": job[1],
    #                 **job[0]
    #             }
    #             jobs_formatted.append(job_formatted)
    #     return jobs_formatted

    def map_jobs(self,jobs):
        jobs_formatted = []
        if jobs:
            for job in jobs:
                job_formatted = {
                    "job_details": job[0],
                    "originalId": job[1],
                    "total_skills": job[2],
                    "matching_skills": job[3],
                    "months_of_experience":job[4],
                    "date_posted":job[5].strftime('%Y-%m-%d') if job[5] else datetime.today(),
                    "skills": job[6],
                    "logo" : job[7],
                }
                jobs_formatted.append(job_formatted)
        return jobs_formatted
    # def tuple_job_into_dictionary(self,jobs):
    #
    #     try:
    #         jobs_json = []
    #
    #         for job in jobs :
    #             job = {
    #                 "id": job[0],
    #                 "original_job_id": job[1],
    #                 "location":job[2],
    #                 "sector_travail":job[3],
    #                 "entreprise":job[4],
    #                 "title":job[5],
    #                 "skills":job[6],
    #                 "months_of_experience": job[7],
    #                 "date_processement":job[8].strftime('%Y-%m-%d'),
    #                 "date_posted":job[9].strftime('%Y-%m-%d'),
    #                 "total_skills": job[10],
    #             }
    #
    #             jobs_json.append(job)
    #
    #         return jobs_json
    #     except Exception as e :
    #         logger.error(f"Error {e}")

    def tuple_job_into_dictionary(self,jobs):

        try:
            jobs_json = []

            for job in jobs :
                job = {
                    "id": job[0],
                    "original_job_id": job[1],
                    "location":job[2],
                    "sector_travail":job[3],
                    "entreprise":job[4],
                    "title":job[5],
                    "skills":job[6],
                    "months_of_experience": job[7],
                    "date_processement":job[8].strftime('%Y-%m-%d'),
                    "date_posted":job[9].strftime('%Y-%m-%d'),
                    "total_skills": job[10],

                }

                jobs_json.append(job)

            return jobs_json
        except Exception as e :
            logger.error(f"Error {e}")

    def tuple_student_into_dictionary(self, student_json):

        student_json = json.loads(student_json)
        profile = student_json["Profil_etudiant"][0]
        info = profile["informations_personnelles"]
        languages = [lang["langue"] for lang in profile["langues"]]
        languages_str = ','.join(languages)
        hard_skills = ','.join(profile["competences"])
        all_skills = hard_skills + ',' + languages_str
        edu = profile["education"][0]
        exp = profile["experience"][0]

        student = {
            "id": profile["id"],
            "informations_personnelles": profile["informations_personnelles"],
            "education": profile["education"][0],  # Take first entry, keep as dict
            "experience": profile["experience"][0],  # Take first entry, keep as dict
            "total_months_experience": profile["total_months_experience"],
            "langues": profile["langues"],  # Keep as list of dicts
            "skills": all_skills  # Add the combined skills field
        }

        return student

    import json
    from datetime import datetime

    def format_candidate(self , candidate_raw):

        total_months_experience = (
            sum(exp.get("total_months_experience", 0) for exp in candidate_raw.get("experiences", []))
            if candidate_raw.get("experiences")
            else 0
        )

        full_name = candidate_raw.get("fullname")
        sexe_map = {"Male": "M", "Female": "F"}
        birthdate_str = candidate_raw.get("birthdate")
        try:
            birthdate_iso = datetime.fromisoformat(birthdate_str).strftime("%Y-%m-%d") if birthdate_str else None
        except Exception:
            birthdate_iso = None

        educations = candidate_raw.get("educations", [])
        formatted_educations = [
            {
                "etablissement": edu.get("school"),
                "diplome": edu.get("degree"),
                "specialisation": edu.get("major"),
            }
            for edu in educations
        ]

        if candidate_raw.get("skills"):
            skills = [
                {
                    "skillName": skill.get("skillName"),
                    "originalID": skill.get("originalID")
                }
                for skill in candidate_raw.get("skills", [])
            ]
        else :
            skills = []

        languages = [
            {
                "langue": lang.get("langue"),
                "niveau": lang.get("level"),
            }
            for lang in candidate_raw.get("languages", [])
        ]

        formatted = {
            "Profil_etudiant": [
                {
                    "id": "1",
                    "informations_personnelles": {
                        "nom_complet": full_name,
                        "email": candidate_raw.get("email"),
                        "numero_de_telephone": candidate_raw.get("phoneNumber"),
                        "ville": candidate_raw.get("city"),
                        "sexe": sexe_map.get(candidate_raw.get("sex"), None),
                        "date_de_naissance": birthdate_iso
                    },
                    "education": formatted_educations,
                    "skills": skills,
                    "total_months_experience": total_months_experience,
                    "langues": languages
                }
            ]
        }

        return formatted

    # def format_student_backend(self, student_raw):
    #     # Helper to format date
    #     def format_date(date_str, to_format="%m/%Y"):
    #         try:
    #             return datetime.strptime(date_str, "%Y-%m-%d").strftime(to_format)
    #         except:
    #             return "En cours"
    #
    #     # Get the latest education info
    #     educations = student_raw.get("educations", [])
    #     education_formatted = []
    #     for edu in educations:
    #         edu_copy = edu.copy()
    #         if "date_de_diplomation" in edu_copy:
    #             try:
    #                 edu_copy["date_de_diplomation"] = datetime.strptime(
    #                     edu_copy["date_de_diplomation"], "%Y-%m-%d"
    #                 ).strftime("%Y")
    #             except:
    #                 edu_copy["date_de_diplomation"] = edu_copy["date_de_diplomation"]
    #         education_formatted.append(edu_copy)
    #
    #     # Format experience
    #     total_months = student_raw.get("total_months_experience")
    #
    #
    #     formatted = {
    #         "Profil_etudiant": [
    #             {
    #                 "id": "1",
    #                 "informations_personnelles": {
    #                     "nom_complet": student_raw.get("nom_complet"),
    #                     "email": student_raw.get("email"),
    #                     "numero_de_telephone": student_raw.get("numero_de_telephone"),
    #                     "ville": student_raw.get("ville"),
    #                     "sexe": student_raw.get("sexe")
    #                 },
    #                 "education": education_formatted,
    #                 "skills": student_raw.get("competences", []),
    #                 "total_months_experience": total_months,
    #                 "langues": student_raw.get("langues", [])
    #             }
    #         ]
    #     }
    #
    #     logger.debug(f"Formated student : {formatted}")
    #     return formatted

    def map_to_jobs_to_swipe(self, jobs ):
        jobs_to_swipe = []
        for job in jobs:
            job_json = {
                "id": job.get("id"),
                "Fonction": job.get("job_details").get("Fonction"),
                "Niveau hiérarchique": job.get("job_details").get("Niveau hiérarchique"),
                "Secteurs": job.get("job_details").get("Secteurs"),
                "Type d’emploi": job.get("job_details").get("Type d’emploi"),
                "description": job.get("job_details").get("description"),
                "entreprise": job.get("job_details").get("entreprise"),
                "joblink": job.get("job_details").get("joblink"),
                "location": job.get("job_details").get("location"),
                "nomberofapplicants": job.get("job_details").get("nomberofapplicants"),
                "time": job.get("job_details").get("time"),
                "title": job.get("job_details").get("title"),
                "months_of_experience": job.get("months_of_experience"),
                "skills": job.get("skills"),
                "total_skills": job.get("total_skills"),
                "logo": job.get("job_details").get("logo_url"),
            }
            jobs_to_swipe.append(job_json)

        return jobs_to_swipe
