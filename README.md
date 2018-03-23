# Anime cast
Это телеграм бот, который транслирует аниме на chromecast. Для запуска нужно заполнить data.json, с логином и паролем от myanimelist, токеном телеграма и токеном вк. Данные от myanimelist нужны для обновления просмотренных эпизодов. Токен от вк нужен, чтобы подтягивать видео от вк, не через их *гейский* плеер. Ну а телеграм токен думаю понятно :)
Примерно как выглядит взаимодействие с ботом:
 - После заполнения data.json можно запускать tg.py
 - Находите своего бота и можете посмотреть список доступных комманд /help
 - Для получения списка аниме, которые находятся у вас в списке на myanimelist с тегом watching нужно написать /get_animes
 - Бот скидывает id; anime_name, cur_watched/all_episodes в таком формате все аниме
 - Отправляете id и бот запускает трансляцию следующего эпизода на хромкаст, видео берет с shikimori
 - Во время трансляции можете отправить боту /pause для паузы, или /play соответственно для проигрывания.

В сурсах так же можно подтягивать картинки анимок, просто я отключил эту функцию т.к. слишком много места занимает. Ах да, бот проверяет кто ему пишет и если логина отправителя нету в tg.py на 16 строке в массиве, то бот ничего делать не будет.

![Violet Evergarden](https://ru.myanimeshelf.com/upload/dynamic/2017-09/04/Violet_Evergarden22.jpg)
