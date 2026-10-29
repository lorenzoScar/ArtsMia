from database.DB_connect import DBConnect
from model.arco import Arco
from model.artObject import ArtObject


class DAO():

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT * 
                FROM object o"""

        cursor.execute(query)

        for row in cursor:
            res.append(ArtObject(**row))
            #creo artobject.py nel model

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getEdgePeso(v1, v2):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                    FROM exhibition_objects eo, exhibition_objects eo2
                    WHERE eo.exhibition_id = eo2.exhibition_id
                    AND eo.object id < eo2.object_id
                    AND eo.object_id = %s AND eo2.object_id = %s
                    GROUP BY eo.object_id, eo2.object_id"""

        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            res.append(row["peso"])

        cursor.close()
        conn.close()

        if len(res) == 0:
            return None
        else:
            return res

    @staticmethod
    def getAllEdges(idMapAO):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []
        query = """SELECT eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                    FROM exhibition_objects eo, exhibition_objects eo2
                    WHERE eo.exhibition_id = eo2.exhibition_id
                    AND eo.object id < eo2.object_id
                    GROUP BY eo.object_id, eo2.object_id
                    ORDER BY peso DESC"""

        cursor.execute(query)

        for row in cursor:
            #res.append((o1, o2, peso))
            #creo arco.py nel model
            res.append(Arco(idMapAO[row["o1"]],idMapAO[row["o2"]],row["peso"]))

        cursor.close()
        conn.close()
        return res