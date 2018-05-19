class ImageURL(object):
    def get_s3_key_prefix(self):
        pass
    def get_s3_tmp_key_prefix(self):
        return "tmp/"


class ProjectAlbumsImageUrl(ImageURL):
    def __init__(self, project_id, album_id):
        self.__project_id = str(project_id)
        self.__album_id = str(album_id)

    def get_s3_key_prefix(self):
        return "projects/" + self.__project_id + "/albums/" + self.__album_id + "/"


class DesignImageURL(ImageURL):
    def __init__(self, design_id):
        self.__design_id = str(design_id)

    def get_s3_key_prefix(self):
        return "designs/" + self.__design_id + "/"

