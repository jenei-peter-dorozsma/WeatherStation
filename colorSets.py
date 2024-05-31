class Colors:
    green = [
        (0, 238, 0, 255),  # Light green: #00ee00
        (0, 142, 0, 255),  # Medium green: #008e00
        (0, 95, 0, 255),   # Darker green: #005f00
        (0, 47, 0, 255),   # Dark green: #002f00
        (0, 0, 0, 0)       # Transparent
    ]

    orange = [
        (237, 169, 61, 255),  # Light orange: #eda93d
        (166, 118, 43, 255),  # Medium orange: #a6762b
        (94, 67, 24, 255),    # Darker orange: #5e4318
        (36, 25, 9, 255),      # Dark orange: #241909
        (0, 0, 0, 0)       # Transparent
    ]

    red = [
        (213, 128, 128, 255),  # #d58080
        (153, 51, 51, 255),    # #993333
        (102, 34, 34, 255),    # #662222
        (51, 17, 17, 255),      # #331111
        (0, 0, 0, 0)       # Transparent
    ]

    yellow = [
        (213, 213, 128, 255),  # #d5d580
        (153, 153, 51, 255),   # #999933
        (102, 102, 34, 255),   # #666622
        (51, 51, 17, 255),      # #333311
        (0, 0, 0, 0)       # Transparent
    ]

    blue = [
        (128, 155, 213, 255),  # #809bd5
        (51, 83, 153, 255),    # #335399
        (34, 56, 102, 255),    # #223866
        (17, 27, 51, 255),      # #111b33
        (0, 0, 0, 0)       # Transparent
    ]

    turquoise = [
        (128, 208, 213, 255),  # #80d0d5
        (51, 147, 153, 255),   # #339399
        (34, 99, 102, 255),    # #226366
        (17, 49, 51, 255),      # #113133
        (0, 0, 0, 0)       # Transparent
    ]

    purple = [
        (180, 128, 213, 255),  # #b480d5
        (113, 51, 153, 255),   # #713399
        (76, 34, 102, 255),    # #4c2266
        (38, 17, 51, 255),      # #261133
        (0, 0, 0, 0)       # Transparent
    ]

    def get_color_set(self, color_set_name):
        color_set = getattr(self, color_set_name, None)
        color_set_normalized = [
            (r / 255.0, g / 255.0, b / 255.0, a / 255.0)
            for (r, g, b, a) in color_set
        ]

        return (color_set, color_set_normalized)


if __name__ == '__main__':
    colors = Colors()
    selected_color_set = "green"
    color_set = colors.get_color_set(selected_color_set)
    print(color_set)