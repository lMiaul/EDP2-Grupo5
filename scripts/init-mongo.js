// scripts/init-mongo.js
// Se ejecuta automáticamente cuando el contenedor mongo inicia por primera vez
// MongoDB ejecuta este archivo solo con volumen vacío (primera ejecución)

db = db.getSiblingDB('cac_valleverde');

// ============================================================
// 1. AGRICULTORES (Datos maestros)
// ============================================================
if (db.agricultores.countDocuments({}) === 0) {
    db.agricultores.insertMany([
        {
            agricultor_id: "agr_1001",
            nombre_completo: "Juan Pérez García",
            dni_ruc: "45678901",
            codigo_productor: "VALLE-VERDE-100",
            sector_comunidad: "Alto Saposoa",
            tipo_cacao: "CCN51",
            certificaciones: ["Orgánico"]
        },
        {
            agricultor_id: "agr_1002",
            nombre_completo: "María Rodríguez López",
            dni_ruc: "12345678",
            codigo_productor: "VALLE-VERDE-101",
            sector_comunidad: "Bajo Progreso",
            tipo_cacao: "Perla Negra",
            certificaciones: ["Orgánico"]
        },
        {
            agricultor_id: "agr_1003",
            nombre_completo: "Carlos Sánchez Martínez",
            dni_ruc: "98765432",
            codigo_productor: "VALLE-VERDE-102",
            sector_comunidad: "El Mirador",
            tipo_cacao: "Pata de Colibrí",
            certificaciones: ["Orgánico"]
        },
        {
            agricultor_id: "agr_1004",
            nombre_completo: "Ana Torres Vásquez",
            dni_ruc: "55667788",
            codigo_productor: "VALLE-VERDE-103",
            sector_comunidad: "Huicungo",
            tipo_cacao: "Trinitario",
            certificaciones: ["Fair Trade"]
        },
        {
            agricultor_id: "agr_1005",
            nombre_completo: "Pedro Quispe Flores",
            dni_ruc: "33445566",
            codigo_productor: "VALLE-VERDE-104",
            sector_comunidad: "Pachiza",
            tipo_cacao: "Forastero",
            certificaciones: []
        }
    ]);
    print("✅ Se insertaron 5 agricultores.");
}

// ============================================================
// 2. USUARIOS (Credenciales de acceso)
// ============================================================
if (db.usuarios.countDocuments({}) === 0) {
    db.usuarios.insertMany([
        {
            email: "acopiador@valleverde.com",
            password: "123",
            rol: "Acopiador",
            nombre: "Operario Demo",
            operario_id: "usr_op_1"
        },
        {
            email: "admin@valleverde.com",
            password: "admin",
            rol: "Administrador",
            nombre: "Gerencia General",
            operario_id: "admin_01"
        }
    ]);
    print("✅ Se insertaron 2 usuarios.");
}

// ============================================================
// 3. ACOPIOS (Registros de demostración para el Dashboard)
// ============================================================
if (db.acopios.countDocuments({}) === 0) {

    // Datos de referencia para generar acopios variados
    var agricultores = [
        { agricultor_id: "agr_1001", nombre_completo: "Juan Pérez García", dni_ruc: "45678901", codigo_productor: "VALLE-VERDE-100", sector_comunidad: "Alto Saposoa", tipo_cacao: "CCN51", certificaciones: ["Orgánico"] },
        { agricultor_id: "agr_1002", nombre_completo: "María Rodríguez López", dni_ruc: "12345678", codigo_productor: "VALLE-VERDE-101", sector_comunidad: "Bajo Progreso", tipo_cacao: "Perla Negra", certificaciones: ["Orgánico"] },
        { agricultor_id: "agr_1003", nombre_completo: "Carlos Sánchez Martínez", dni_ruc: "98765432", codigo_productor: "VALLE-VERDE-102", sector_comunidad: "El Mirador", tipo_cacao: "Pata de Colibrí", certificaciones: ["Orgánico"] },
        { agricultor_id: "agr_1004", nombre_completo: "Ana Torres Vásquez", dni_ruc: "55667788", codigo_productor: "VALLE-VERDE-103", sector_comunidad: "Huicungo", tipo_cacao: "Trinitario", certificaciones: ["Fair Trade"] },
        { agricultor_id: "agr_1005", nombre_completo: "Pedro Quispe Flores", dni_ruc: "33445566", codigo_productor: "VALLE-VERDE-104", sector_comunidad: "Pachiza", tipo_cacao: "Forastero", certificaciones: [] }
    ];

    var fermentaciones = ["Tipo 1 (Premium)", "Tipo 2 (Estándar)"];
    var almacenes = ["ZONA-A-SECO", "ZONA-B-SECADO", "ZONA-C-CUARENTENA"];
    var dispositivos = ["Tablet-Android-01", "Tablet-Android-02", "Terminal-Web-01"];
    var estados_pago = ["Pendiente", "Pagado"];
    var precio_base = 12.00;

    var acopios = [];
    var now = new Date();

    for (var i = 0; i < 20; i++) {
        // Seleccionar agricultor cíclicamente para distribución equilibrada
        var agric = agricultores[i % agricultores.length];

        // Fecha aleatoria en los últimos 30 días
        var diasAtras = Math.floor(Math.random() * 30);
        var fecha = new Date(now.getTime() - (diasAtras * 24 * 60 * 60 * 1000));

        // Simular sacos (entre 1 y 5)
        var cantidad_sacos = Math.floor(Math.random() * 5) + 1;
        var detalle_sacos = [];
        var peso_bruto_total = 0;
        var tara_unitaria = 0.5;

        for (var s = 0; s < cantidad_sacos; s++) {
            var peso_saco = Math.round((45 + Math.random() * 20) * 100) / 100;
            detalle_sacos.push({ nro_saco: s + 1, peso_bruto_kg: peso_saco });
            peso_bruto_total += peso_saco;
        }

        peso_bruto_total = Math.round(peso_bruto_total * 100) / 100;
        var tara_total = cantidad_sacos * tara_unitaria;
        var peso_neto = Math.round((peso_bruto_total - tara_total) * 100) / 100;

        // Calidad
        var humedad = Math.round((6 + Math.random() * 4) * 10) / 10;
        var impurezas = Math.round((0.5 + Math.random() * 2.5) * 10) / 10;
        var estado_lote = humedad <= 8.0 ? "Aprobado" : "Observado (Requiere secado)";

        // Finanzas
        var bono_cert = agric.certificaciones.indexOf("Orgánico") >= 0 ? 1.50 : 0.0;
        var descuento_hum = humedad > 8.0 ? 0.50 : 0.0;
        var precio_final = precio_base + bono_cert - descuento_hum;
        var monto_total = Math.round(peso_neto * precio_final * 100) / 100;

        var ticketNum = String(i + 1).padStart(4, '0');
        var mesAbrev = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"][fecha.getMonth()];

        acopios.push({
            codigo_ticket: "TK-2026-" + ticketNum,
            fecha_registro: fecha,
            operario_id: "usr_op_" + (Math.floor(Math.random() * 3) + 1),
            agricultor: {
                agricultor_id: agric.agricultor_id,
                nombre_completo: agric.nombre_completo,
                dni_ruc: agric.dni_ruc,
                codigo_productor: agric.codigo_productor,
                certificaciones: agric.certificaciones,
                sector_comunidad: agric.sector_comunidad,
                tipo_cacao: agric.tipo_cacao
            },
            datos_pesaje: {
                cantidad_sacos: cantidad_sacos,
                detalle_sacos: detalle_sacos,
                peso_bruto_total_kg: peso_bruto_total,
                tara_total_kg: tara_total,
                peso_neto_total_kg: peso_neto
            },
            control_calidad: {
                porcentaje_humedad: humedad,
                porcentaje_impurezas: impurezas,
                grado_fermentacion: fermentaciones[Math.floor(Math.random() * fermentaciones.length)],
                estado_lote: estado_lote
            },
            valores_comerciales: {
                precio_base_por_kilo: precio_base,
                bonificacion_certificacion: bono_cert,
                descuento_humedad: descuento_hum,
                precio_final_por_kilo: precio_final,
                monto_total_pagar: monto_total
            },
            trazabilidad: {
                codigo_lote_exportacion: "LOTE-EXP-2026-" + mesAbrev + "-" + (Math.floor(Math.random() * 5) + 1),
                ubicacion_almacen: almacenes[Math.floor(Math.random() * almacenes.length)]
            },
            metadata_sistema: {
                dispositivo_registro: dispositivos[Math.floor(Math.random() * dispositivos.length)],
                estado_pago: estados_pago[Math.floor(Math.random() * estados_pago.length)],
                ultima_modificacion: fecha
            }
        });
    }

    db.acopios.insertMany(acopios);
    print("✅ Se insertaron " + acopios.length + " registros de acopio.");
}

print("🎉 Seed de base de datos completado.");
