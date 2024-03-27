# Copyright 2024 ritik
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("title", "authors", "publication_date", "isbn", "description")

    def validate(self, data):
        if len(data["title"]) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        if len(data["authors"]) == 0:
            raise serializers.ValidationError("At least one author must be specified.")
        if data["publication_date"] > datetime.date.today():
            raise serializers.ValidationError("Publication date cannot be in the future.")
        if len(data["isbn"]) != 13:
            raise serializers.ValidationError("ISBN must be 13 characters long.")
        if len(data["description"]) > 1000:
            raise serializers.ValidationError("Description cannot exceed 1000 characters.")
        return data