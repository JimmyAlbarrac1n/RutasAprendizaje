from app import mongo

class LearningRouteModel:
    @staticmethod
    def create_route(route_data):
        return mongo.db.learning_routes.insert_one(route_data)

    @staticmethod
    def get_all_routes():
        return list(mongo.db.learning_routes.find())

    @staticmethod
    def update_route(route_id, update_data):
        return mongo.db.learning_routes.update_one({"_id": route_id}, {"$set": update_data})

    @staticmethod
    def delete_route(route_id):
        return mongo.db.learning_routes.delete_one({"_id": route_id})
