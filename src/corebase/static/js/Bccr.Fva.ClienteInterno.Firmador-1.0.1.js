"use strict";
var FvaClienteInterno = function(m) {
    this.AsigneElTextoALaVentana = s;
    this.MuestreLaVentanaModal = f;
    this.OculteLaVentanaModal = n;
    this.MuestreElBotonDeAceptar = l;
    this.OculteElBotonDeAceptar = A;
    this.MuestreLaAnimacionDeEspera = g;
    this.OculteLaAnimacionDeEspera = D;
    this.MuestreElBordeDeError = p;
    this.RemuevaElBordeDeError = q;
    this.EnvieLaSolicitud = v;
    var F = $("<div>", {
        "class": "fvaBoton"
    }).html("Aceptar");
    var E = $("<div>", {
        "class": "fvaFondoOscuro"
    });
    var e = $("<div>", {
        "class": "fvaVentanaModal"
    }).css({
        display: "none"
    });
    var i = $("<div>", {
        "class": "fvaContenidoVentanaModal"
    });
    var j = $("<div>", {
        "class": "fvaMargenDeContenido"
    });
    var c = $("<div>", {
        "class": "fvaContenidoDeCopieCodigo"
    });
    var z = $("<div>", {
        "class": "fvaAcordeon"
    });
    var t = $("<div>", {
        "class": "fvaPanelAcordeon"
    });
    var o = $("<span>", {
        "class": "fvaToolTipText"
    });
    var C = $("<div>", {
        "class": "fvaCodigoConBotonCopiar"
    });
    var h = $("<div>", {
        "class": "fvaLoader"
    }).append($("<div>"), $("<div>"), $("<div>"));
    var x = $("<div>", {
        "class": "fvaElementoOculto"
    });
    var y = $("<input/>", {
        "class": "fvaElementoOculto"
    });
    var u = $("<div>", {
        "class": "fvaMensajeDeCopiado"
    }).css({
        display: "none"
    });
    var w = "Copie el c&oacute;digo de verificaci&oacute;n en el Firmador BCCR";
    var k = "&iquest;Qu&eacute; es el Firmador BCCR?";
    var d = '<div class="fvaDescripcionDelFormato"><span class="fvaCodLetra">Letra</span><span class="fvaDescripcionDelFormatoSeparador"> | </span><span>N&uacute;mero</span></div>';
    var b = $("<img>", {
        src: m.images.ayuda,
        alt: "Ayuda",
        height: "21",
        width: "21"
    });
    var r = $("<div>", {
        "class": "fvaContenidoDeTextoCopieElCodigo"
    });
    var G = m.urlconsultafirma;
    var a = $("<input/>", {
        "class": "fvaElBotonDeCopiar",
        value: "Copiar",
        type: "button"
    });
    B();

    function B() {
        F.bind("click", H);
        $("body").append(e);
        $("body").append(E);
        $("body").append(x);
        $("body").append(y);
        $("body").append(u);
        I();

        function I() {
            J();
            i.append(j, h, F);
            e.append(i);

            function J() {
                $("head").append('<link rel="stylesheet" href="' + m.urlcss+ '" type="text/css" />');
            }
        }

        function H() {
            n();
            m.SolicitudNoRealizada();
        }
    }

    function v() {
        q();
        s(m.TextoSolicitando);
        A();
        g();
        f();
        I();

        function I() {
            var O = m.DatosParaSolicitar();
            $.ajax({
                url: m.UrlParaSolicitar,
                type: "POST",
                dataType: "text json",
                processData: false,
                data: O,
                contentType: false,
                cache: false,
                global: false,
                success: N,
                error: K
            });
        }

        function N(W) {
            var Y = W.FueExitosaLaSolicitud;
            var X = Z(W.TiempoMaximoDeFirmaEnSegundos);
            var T = Z(W.TiempoDeEsperaParaConsultarLaFirmaEnSegundos);
            var aa = W.CodigoDeVerificacion;
            var V = W.IdDeLaSolicitud;
            var ac = false;
            if (Y) {
                var O = Q(aa);
                C.html("").append(O, a);
                ab();
                var ad = R();
                s(ad);
                P();
            } else {
                M(W);
            }

            function R() {
                r.html(w);
                z.append(b, o);
                t.append(m.ImagenDelFirmador);
                c.append(r, z);
                t.css({
                    "max-height": "0px"
                });
                z.removeClass("active");
                o.html(k);
                z.click(function() {
                    this.classList.toggle("active");
                    if (t[0].style.maxHeight != "0px") {
                        t[0].style.maxHeight = "0px";
                        o.html(k);
                    } else {
                        t[0].style.maxHeight = t[0].scrollHeight + "px";
                        o.html("Ocultar");
                    }
                });
                a.click(af);
                var ah = $("<div>").append(c, C, d, t);
                return ah;
            }

            function af() {
                y.val(aa);
                y.select();
                var aj = "";
                try {
                    var ah = document.execCommand("copy");
                    if (ah) {
                        aj = "C&oacute;digo de verificaci&oacute;n copiado";
                    } else {
                        aj = "No se ha podido copiar el c&oacute;digo de verificaci&oacute;n";
                    }
                } catch (ai) {
                    aj = "No se ha podido copiar el c&oacute;digo de verificaci&oacute;n";
                }
                u.html(aj);
                if (u[0].style.display !== "block") {
                    u.fadeIn("slow", function() {
                        $(this).delay(1500).fadeOut("slow");
                    });
                }
            }

            function ab() {
                setTimeout(S, X);
            }

            function S() {
                ac = true;
            }

            function Z(ah) {
                return 1000 * parseInt(ah);
            }

            function Q(ak) {
                var ai = "<div>";
                var am;
                var aj;
                var ah = ak.length;
                for (var al = 0; al < ah; al++) {
                    aj = ak[al];
                    if (ag(aj)) {
                        am = "<span>" + aj + "</span>";
                    } else {
                        am = '<span class="fvaCodLetra">' + aj + "</span>";
                    }
                    ai = ai + am;
                }
                return ai + "</div>";
            }

            function ag(ah) {
                return !isNaN(ah);
            }

            function ae() {
                var ah = {
                    IdDeLaSolicitud: V
                };
                $.ajax({
                    url: G,
                    jsonp: "callback",
                    dataType: "jsonp",
                    data: ah,
                    global: false,
                    success: U,
                    error: K
                });
            }

            function P() {
                setTimeout(ae, T);
            }

            function U(ah) {
                if (ah.SeRealizo == true) {
                    J(ah);
                } else {
                    if (ac == true) {
                        K();
                    } else {
                        P();
                    }
                }
            }
        }

        function J(O) {
            if (O.FueExitosa == true) {
                L();
            } else {
                M(O);
            }
        }

        function M(O) {
            if (O.DebeMostrarElError == true) {
                var P = m.MensajeDeError + '<div class="fvaMargenDeContenido fvaColorMensajeSecundario">' + O.DescripcionDelError + "</div>";
                H(P);
            } else {
                H(m.MensajeDeError);
            }
        }

        function L() {
            n();
            m.SolicitudRealizada();
        }

        function K() {
            H(m.MensajeDeError);
        }

        function H(O) {
            p();
            s(O);
            D();
            l();
        }
    }

    function s(H) {
        j.html(H);
        I(H);

        function I(J) {
            var K = $("<input/>", {
                type: "text"
            });
            K.val(J);
            x.empty();
            x.append(K);
            K.focus();
        }
    }

    function f() {
        E.css({
            display: "block"
        });
        e.css({
            display: "block"
        });
    }

    function A() {
        F.css({
            display: "none"
        });
    }

    function g() {
        h.css({
            display: "block"
        });
    }

    function n() {
        E.css({
            display: "none"
        });
        e.css({
            display: "none"
        });
    }

    function D() {
        h.css({
            display: "none"
        });
    }

    function l() {
        F.css({
            display: "inline-block"
        });
    }

    function q() {
        i.removeClass("fvaBordeDeError");
    }

    function p() {
        i.addClass("fvaBordeDeError");
    }
};
var FvaAutenticador = function(t) {
    var funcs={
	AutenticacionRealizada: t.AutenticacionRealizada,
	ObtengaLosDatosParaSolicitarLaAutenticacion: t.ObtengaLosDatosParaSolicitarLaAutenticacion,
	AutenticacionNoRealizada: t.AutenticacionNoRealizada
	}
    t = $.extend({
        MensajeDeError: "Ocurri&oacute; un error al realizar la autenticaci&oacute;n."
    }, t);
    var o = $("#" + t.IdDelBotonDeAutenticar);
    var h = $("<img>", {
        src: t.images.autenticador,
        alt: "Imagen de ayuda del Autenticador"
    });
    var s = $.extend(t, {
        TextoSolicitando: "Procesando su solicitud de autenticaci&oacute;n...",
        ImagenDelFirmador: h,
        DatosParaSolicitar: l,
        UrlParaSolicitar: t.UrlParaSolicitarLaAutenticacion,
        SolicitudRealizada: funcs.AutenticacionRealizada,
        ObtengaLosDatosParaSolicitarLaAutenticacion: funcs.ObtengaLosDatosParaSolicitarLaAutenticacion,
        SolicitudNoRealizada: funcs.AutenticacionNoRealizada
    });

    var b = "<div class='fvaToolTipIdentificacionTitulo'>Formato de la identificaci&oacute;n</div><ul><li><span>Nacional:</span><span>00-0000-0000</span></li><li><span>DIDI:</span><span>500000000000</span></li><li><span>DIMEX:</span><span>100000000000</span></li></li>";
    var n = "Para autenticarse " + t.ParaAutenticarse + ", primero debe ingresar su n&uacute;mero de identificaci&oacute;n:";
    var j = $("<input>", {
        type: "text"
    });
    var g = $("<div>", {
        "class": "fvaMensajeErrorIdentificacion fvaMargenDeContenido"
    });
    var a = $("<div>", {
        "class": "fvaBoton"
    });
    var m = $("<div>", {
        "class": "fvaBoton"
    });
    var d = $("<div>", {
        "class": "fvaMargenDeContenido"
    });
    var u = $("<div>", {
        "class": "fvaContenidoParaIdentificacion"
    });
    var q = $("<div>", {
        "class": "fvaPosicionDelToolTipIdentificacion"
    });
    var k = $("<div>", {
        "class": "fvaToolTipIdentificacion"
    });
    var p = $("<div>", {
        "class": "fvaMargenDeContenido"
    });
    var r = $("<div>", {
        "class": "fvaContenidoParaTipoIdentificacion"
    });
    var c = $("<div>", {
        "class": "fvaRadioBoton"
    });
    var i = $("<div>", {
        "class": "fvaRadioBoton"
    });
    var f = new FvaClienteInterno(s);
    o.click(function() {
        var w = e();
        f.RemuevaElBordeDeError();
        f.AsigneElTextoALaVentana(w);
        f.OculteElBotonDeAceptar();
        f.OculteLaAnimacionDeEspera();
        f.MuestreLaVentanaModal();
    });

    function e() {
        var w = $("<div>");
        a.html("Autenticar");
        m.html("Cancelar");
        c.html("<input type='radio' name='laOpcionNacional' id ='laOpcionNacional' value='laOpcionNacional' checked>Nacional ");
        i.html("<input type='radio' name='laOpcionExtranjero' id ='laOpcionExtranjero' value='laOpcionExtranjero'>Extranjero");
        p.html(n);
        k.html(b);
        q.append(k);
        u.append(j, q);
        r.append(c, i);
        d.append(a, m);
        j.val("");
        g.html("");
        a.click(function() {
            v();
        });
        j.keyup(function(x) {
            if (x.keyCode === 13) {
                v();
            }
            if ((j.val().length > 1) && (j.val().startsWith("0") == false) && ($("#laOpcionNacional").is(":checked"))) {
                j.val("");
            }
            if ((j.val().length > 1) && (j.val().startsWith("5") == false) && (j.val().startsWith("1") == false) && ($("#laOpcionExtranjero").is(":checked"))) {
                j.val("");
            }
            if ((j.val().length == 1) && (j.val() != "0") && ($("#laOpcionNacional").is(":checked"))) {
                j.val("0" + j.val());
            }
            if ((j.val().length == 1) && (j.val() != "5") && (j.val() != "1") && ($("#laOpcionExtranjero").is(":checked"))) {
                j.val("");
            }
        });
        m.click(function() {
            f.OculteLaVentanaModal();
        });
        c.click(function() {
            $("#laOpcionNacional").prop("checked", true);
            j.maskCI("00-0000-0000", {
                reverse: true,
                placeholder: "00-0000-0000"
            });
            j.val("");
            $("#laOpcionExtranjero").prop("checked", false);
        });
        i.click(function() {
            $("#laOpcionExtranjero").prop("checked", true);
            j.maskCI("000000000000", {
                reverse: true,
                placeholder: "000000000000"
            });
            j.val("");
            $("#laOpcionNacional").prop("checked", false);
        });
        w.append(p, u, r, g, d);
        j.maskCI("00-0000-0000", {
            reverse: true,
            placeholder: "00-0000-0000"
        });
        return w;
    }

    function v() {
        var x = w();
        if (x) {
            f.EnvieLaSolicitud();
        } else {
            f.MuestreElBordeDeError();
            g.html("El formato de la identificaci&oacute;n es incorrecto.");
        }

        function w() {
            var y = j.val();
            return FvaValidador.ValideLaIdentificacion(y);
        }
    }

    function l() {
        var x = t.ObtengaLosDatosParaSolicitarLaAutenticacion();
        var w = j.val();
        if (x === undefined) {
            x = new FormData();
        }
        x.append("Identificacion", w);
        return x;
    }
};
var FvaFirmador = function(e) {
    e = $.extend({
        MensajeDeError: "Ocurri&oacute; un error al realizar la firma."
    }, e);
    var d = $("#" + e.IdDelBotonDeFirmar);
    var b = $("<img>", {
        src: e.images.firma,
        alt: "Imagen de ayuda del Firmador"
    });
    var a =  $.extend(e, {
        TextoSolicitando: "Procesando su solicitud de firma...",
        ImagenDelFirmador: b,
        DatosParaSolicitar: f,
        SolicitudRealizada: e.FirmaRealizada,
        SolicitudNoRealizada: e.FirmaNoRealizada
    });
    var c = new FvaClienteInterno(a);
    d.click(function() {
        c.EnvieLaSolicitud();
    });

    function f() {
        return e.ObtengaLosDatosParaSolicitarLaFirma();
    }
};
var FvaValidador = {
    ValideLaIdentificacion: function(b) {
        var e = /^0[1-9]{1}-\d{4}-\d{4}$/;
        var a = /^5[0-9]{11}$/;
        var c = /^1[0-9]{11}$/;
        var d;
        if (e.test(b) || a.test(b) || c.test(b)) {
            d = true;
        } else {
            d = false;
        }
        return d;
    }
};
(function(a, c, b) {
    if (typeof define === "function" && define.amd) {
        define(["jquery"], a);
    } else {
        if (typeof exports === "object") {
            module.exports = a(require("jquery"));
        } else {
            a(c || b);
        }
    }
}(function(b) {
    var c = function(l, i, g) {
        var k = {
            invalid: [],
            getCaret: function() {
                try {
                    var p, o = 0,
                        r = l.get(0),
                        n = document.selection,
                        s = r.selectionStart;
                    if (n && navigator.appVersion.indexOf("MSIE 10") === -1) {
                        p = n.createRange();
                        p.moveStart("character", -k.val().length);
                        o = p.text.length;
                    } else {
                        if (s || s === "0") {
                            o = s;
                        }
                    }
                    return o;
                } catch (q) {}
            },
            setCaret: function(o) {
                try {
                    if (l.is(":focus")) {
                        var p, q = l.get(0);
                        if (q.setSelectionRange) {
                            q.setSelectionRange(o, o);
                        } else {
                            p = q.createTextRange();
                            p.collapse(true);
                            p.moveEnd("character", o);
                            p.moveStart("character", o);
                            p.select();
                        }
                    }
                } catch (n) {}
            },
            events: function() {
                l.on("keydown.maskCI", function(n) {
                    l.data("maskCI-keycode", n.keyCode || n.which);
                    l.data("maskCI-previus-value", l.val());
                    l.data("maskCI-previus-caret-pos", k.getCaret());
                    k.maskDigitPosMapOld = k.maskCIDigitPosMap;
                }).on(b.jMaskGlobals.useInput ? "input.maskCI" : "keyup.maskCI", k.behaviour).on("paste.maskCI drop.maskCI", function() {
                    setTimeout(function() {
                        l.keydown().keyup();
                    }, 100);
                }).on("change.maskCI", function() {
                    l.data("changed", true);
                }).on("blur.maskCI", function() {
                    if (h !== k.val() && !l.data("changed")) {
                        l.trigger("change");
                    }
                    l.data("changed", false);
                }).on("blur.maskCI", function() {
                    h = k.val();
                }).on("focus.maskCI", function(n) {
                    if (g.selectOnFocus === true) {
                        b(n.target).select();
                    }
                }).on("focusout.maskCI", function() {
                    if (g.clearIfNotMatch && !m.test(k.val())) {
                        k.val("");
                    }
                });
            },
            getRegexMask: function() {
                var v = [],
                    t, n, q, o, p, s;
                for (var u = 0; u < i.length; u++) {
                    t = j.translation[i.charAt(u)];
                    if (t) {
                        n = t.pattern.toString().replace(/.{1}$|^.{1}/g, "");
                        q = t.optional;
                        o = t.recursive;
                        if (o) {
                            v.push(i.charAt(u));
                            p = {
                                digit: i.charAt(u),
                                pattern: n
                            };
                        } else {
                            v.push(!q && !o ? n : (n + "?"));
                        }
                    } else {
                        v.push(i.charAt(u).replace(/[-\/\\^$*+?.()|[\]{}]/g, "\\$&"));
                    }
                }
                s = v.join("");
                if (p) {
                    s = s.replace(new RegExp("(" + p.digit + "(.*" + p.digit + ")?)"), "($1)?").replace(new RegExp(p.digit, "g"), p.pattern);
                }
                return new RegExp(s);
            },
            destroyEvents: function() {
                l.off(["input", "keydown", "keyup", "paste", "drop", "blur", "focusout", ""].join(".maskCI "));
            },
            val: function(q) {
                var n = l.is("input"),
                    p = n ? "val" : "text",
                    o;
                if (arguments.length > 0) {
                    if (l[p]() !== q) {
                        l[p](q);
                    }
                    o = l;
                } else {
                    o = l[p]();
                }
                return o;
            },
            calculateCaretPosition: function() {
                var r = l.data("maskCI-previus-value") || "",
                    t = k.getMasked(),
                    o = k.getCaret();
                if (r !== t) {
                    var y = l.data("maskCI-previus-caret-pos") || 0,
                        u = t.length,
                        s = r.length,
                        v = 0,
                        w = 0,
                        p = 0,
                        q = 0,
                        n = 0;
                    for (n = o; n < u; n++) {
                        if (!k.maskCIDigitPosMap[n]) {
                            break;
                        }
                        w++;
                    }
                    for (n = o - 1; n >= 0; n--) {
                        if (!k.maskCIDigitPosMap[n]) {
                            break;
                        }
                        v++;
                    }
                    for (n = o - 1; n >= 0; n--) {
                        if (k.maskCIDigitPosMap[n]) {
                            p++;
                        }
                    }
                    for (n = y - 1; n >= 0; n--) {
                        if (k.maskDigitPosMapOld[n]) {
                            q++;
                        }
                    }
                    if (o > s) {
                        o = u;
                    } else {
                        if (y >= o && y !== s) {
                            if (!k.maskDigitPosMapOld[o]) {
                                var x = o;
                                o -= q - p;
                                o -= v;
                                if (k.maskCIDigitPosMap[o]) {
                                    o = x;
                                }
                            }
                        } else {
                            if (o > y) {
                                o += p - q;
                                o += w;
                            }
                        }
                    }
                }
                return o;
            },
            behaviour: function(q) {
                q = q || window.event;
                k.invalid = [];
                var o = l.data("maskCI-keycode");
                if (b.inArray(o, j.byPassKeys) === -1) {
                    var p = k.getMasked(),
                        n = k.getCaret();
                    setTimeout(function() {
                        k.setCaret(k.calculateCaretPosition());
                    }, 10);
                    k.val(p);
                    k.setCaret(n);
                    return k.callbacks(q);
                }
            },
            getMasked: function(q, w) {
                var B = [],
                    A = w === undefined ? k.val() : w + "",
                    C = 0,
                    u = i.length,
                    y = 0,
                    t = A.length,
                    r = 1,
                    G = "push",
                    F = -1,
                    H = 0,
                    x = [],
                    p, E;
                if (g.reverse) {
                    G = "unshift";
                    r = -1;
                    p = 0;
                    C = u - 1;
                    y = t - 1;
                    E = function() {
                        return C > -1 && y > -1;
                    };
                } else {
                    p = u - 1;
                    E = function() {
                        return C < u && y < t;
                    };
                }
                var n;
                while (E()) {
                    var D = i.charAt(C),
                        o = A.charAt(y),
                        s = j.translation[D];
                    if (s) {
                        if (o.match(s.pattern)) {
                            B[G](o);
                            if (s.recursive) {
                                if (F === -1) {
                                    F = C;
                                } else {
                                    if (C === p) {
                                        C = F - r;
                                    }
                                }
                                if (p === F) {
                                    C -= r;
                                }
                            }
                            C += r;
                        } else {
                            if (o === n) {
                                H--;
                                n = undefined;
                            } else {
                                if (s.optional) {
                                    C += r;
                                    y -= r;
                                } else {
                                    if (s.fallback) {
                                        B[G](s.fallback);
                                        C += r;
                                        y -= r;
                                    } else {
                                        k.invalid.push({
                                            p: y,
                                            v: o,
                                            e: s.pattern
                                        });
                                    }
                                }
                            }
                        }
                        y += r;
                    } else {
                        if (!q) {
                            B[G](D);
                        }
                        if (o === D) {
                            x.push(y);
                            y += r;
                        } else {
                            n = D;
                            x.push(y + H);
                            H++;
                        }
                        C += r;
                    }
                }
                var z = i.charAt(p);
                if (u === t + 1 && !j.translation[z]) {
                    B.push(z);
                }
                var I = B.join("");
                k.mapMaskdigitPositions(I, x, t);
                return I;
            },
            mapMaskdigitPositions: function(r, o, n) {
                var q = g.reverse ? r.length - n : 0;
                k.maskCIDigitPosMap = {};
                for (var p = 0; p < o.length; p++) {
                    k.maskCIDigitPosMap[o[p] + q] = 1;
                }
            },
            callbacks: function(r) {
                var o = k.val(),
                    n = o !== h,
                    p = [o, r, l, g],
                    q = function(u, s, t) {
                        if (typeof g[u] === "function" && s) {
                            g[u].apply(this, t);
                        }
                    };
                q("onChange", n === true, p);
                q("onKeyPress", n === true, p);
                q("onComplete", o.length === i.length, p);
                q("onInvalid", k.invalid.length > 0, [o, r, l, k.invalid, g]);
            }
        };
        l = b(l);
        var j = this,
            h = k.val(),
            m;
        i = typeof i === "function" ? i(k.val(), undefined, l, g) : i;
        j.maskCI = i;
        j.options = g;
        j.remove = function() {
            var n = k.getCaret();
            k.destroyEvents();
            k.val(j.getCleanVal());
            k.setCaret(n);
            return l;
        };
        j.getCleanVal = function() {
            return k.getMasked(true);
        };
        j.getMaskedVal = function(n) {
            return k.getMasked(false, n);
        };
        j.init = function(n) {
            n = n || false;
            g = g || {};
            j.clearIfNotMatch = b.jMaskGlobals.clearIfNotMatch;
            j.byPassKeys = b.jMaskGlobals.byPassKeys;
            j.translation = b.extend({}, b.jMaskGlobals.translation, g.translation);
            j = b.extend(true, {}, j, g);
            m = k.getRegexMask();
            if (n) {
                k.events();
                k.val(k.getMasked());
            } else {
                if (g.placeholder) {
                    l.attr("placeholder", g.placeholder);
                }
                if (l.data("maskCI")) {
                    l.attr("autocomplete", "off");
                }
                for (var o = 0, r = true; o < i.length; o++) {
                    var p = j.translation[i.charAt(o)];
                    if (p && p.recursive) {
                        r = false;
                        break;
                    }
                }
                if (r) {
                    l.attr("maxlength", i.length);
                }
                k.destroyEvents();
                k.events();
                var q = k.getCaret();
                k.val(k.getMasked());
                k.setCaret(q);
            }
        };
        j.init(!l.is("input"));
    };
    b.maskWatchers = {};
    var e = function() {
            var h = b(this),
                j = {},
                i = "data-maskCI-",
                g = h.attr("data-maskCI");
            if (h.attr(i + "reverse")) {
                j.reverse = true;
            }
            if (h.attr(i + "clearifnotmatch")) {
                j.clearIfNotMatch = true;
            }
            if (h.attr(i + "selectonfocus") === "true") {
                j.selectOnFocus = true;
            }
            if (f(h, g, j)) {
                return h.data("maskCI", new c(this, g, j));
            }
        },
        f = function(g, j, h) {
            h = h || {};
            var i = b(g).data("maskCI"),
                l = JSON.stringify,
                k = b(g).val() || b(g).text();
            try {
                if (typeof j === "function") {
                    j = j(k);
                }
                return typeof i !== "object" || l(i.options) !== l(h) || i.maskCI !== j;
            } catch (m) {}
        },
        a = function(g) {
            var h = document.createElement("div"),
                i;
            g = "on" + g;
            i = (g in h);
            if (!i) {
                h.setAttribute(g, "return;");
                i = typeof h[g] === "function";
            }
            h = null;
            return i;
        };
    b.fn.maskCI = function(i, h) {
        h = h || {};
        var g = this.selector,
            j = b.jMaskGlobals,
            l = j.watchInterval,
            k = h.watchInputs || j.watchInputs,
            m = function() {
                if (f(this, i, h)) {
                    return b(this).data("maskCI", new c(this, i, h));
                }
            };
        b(this).each(m);
        if (g && g !== "" && k) {
            clearInterval(b.maskWatchers[g]);
            b.maskWatchers[g] = setInterval(function() {
                b(document).find(g).each(m);
            }, l);
        }
        return this;
    };
    b.fn.masked = function(g) {
        return this.data("maskCI").getMaskedVal(g);
    };
    b.fn.unmask = function() {
        clearInterval(b.maskWatchers[this.selector]);
        delete b.maskWatchers[this.selector];
        return this.each(function() {
            var g = b(this).data("maskCI");
            if (g) {
                g.remove().removeData("maskCI");
            }
        });
    };
    b.fn.cleanVal = function() {
        return this.data("maskCI").getCleanVal();
    };
    b.applyDataMask = function(g) {
        g = g || b.jMaskGlobals.maskElements;
        var h = (g instanceof b) ? g : b(g);
        h.filter(b.jMaskGlobals.dataMaskAttr).each(e);
    };
    var d = {
        maskElements: "input,td,span,div",
        dataMaskAttr: "*[data-maskCI]",
        dataMask: true,
        watchInterval: 300,
        watchInputs: true,
        useInput: !/Chrome\/[2-4][0-9]|SamsungBrowser/.test(window.navigator.userAgent) && a("input"),
        watchDataMask: false,
        byPassKeys: [9, 16, 17, 18, 36, 37, 38, 39, 40, 91],
        translation: {
            "0": {
                pattern: /\d/
            },
            "9": {
                pattern: /\d/,
                optional: true
            },
            "#": {
                pattern: /\d/,
                recursive: true
            },
            A: {
                pattern: /[a-zA-Z0-9]/
            },
            S: {
                pattern: /[a-zA-Z]/
            }
        }
    };
    b.jMaskGlobals = b.jMaskGlobals || {};
    d = b.jMaskGlobals = b.extend(true, {}, d, b.jMaskGlobals);
    if (d.dataMask) {
        b.applyDataMask();
    }
    setInterval(function() {
        if (b.jMaskGlobals.watchDataMask) {
            b.applyDataMask();
        }
    }, d.watchInterval);
}, window.jQuery, window.Zepto));
