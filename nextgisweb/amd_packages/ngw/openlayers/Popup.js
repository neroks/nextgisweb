define([
    "dojo/dom-construct",
    "dojo/dom-style",
    "dojo/dom-geometry",
    "./../openlayers",
], function (
    domConstruct,
    domStyle,
    domGeom,
    openlayers
) {
    var Popup = OpenLayers.Class(OpenLayers.Popup, {
        displayClass: "ngwPopup dijitTooltipBelow",
        contentDisplayClass: "dijitTooltipContainer",
        padding: new OpenLayers.Bounds([2, 2, 2, 36]),

        setBorder: function () {
            // заглушка, чтобы OL не портили popup border
        },

        initialize: function(params) {
            OpenLayers.Popup.prototype.initialize.apply(this, [
                params.id,
                params.point,
                new openlayers.Size(params.size[0], params.size[1]),
                null,
                null,
                null
            ]);

            this.title = params.title;

            // Сдвигаем карту в случае, если popup выходит за границу 
            this.panMapIfOutOfView = true;

            // СontentDiv, который создает родительский класс
            // мы используем для внутренних нужд.
            this._contentDiv = this.contentDiv;
            domStyle.set(this._contentDiv, {
                width: "auto",
                height: "auto",
                padding: "0"
            })

            // Создаем свой contentDiv
            this.contentDiv = domConstruct.create("div", {
                style: {
                    width: params.size[0],
                    height: params.size[1],
                    padding: "0",
                    margin: "1px"
                }
            }, this._contentDiv, "last");

            // Заголовок
            this.titleDiv = domConstruct.create("div", {
                innerHTML: this.title ? this.title : "&nbsp;",
                style: "background-color: #eee; margin: 1px 1px 2px 1px;"
            }, this._contentDiv, "first");

            // Кнопка закрытия в заголовке
            this._closeSpan = domConstruct.create("span", {
                class: "dijitDialogCloseIcon",
                style: "margin-top: 2px"
            }, this.titleDiv, "last");

            // Соединительная стрелка
            this._connectorDiv = domConstruct.create("div", {
                class: "dijitTooltipConnector"
            }, this.div, 'first');
        },

        draw: function (px) {
            var result = OpenLayers.Popup.prototype.draw.apply(this, arguments);
            domStyle.set(result, "background", "rgba(255, 255, 255, 0)");
            return result;
        },

        moveTo: function (px) {
            px.x = px.x - 12;
            px.y = px.y - 8;
            OpenLayers.Popup.prototype.moveTo.apply(this, [px]);
        }

    });

    return Popup;
});
