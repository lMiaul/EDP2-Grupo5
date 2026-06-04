// scripts/init-mongo.js
// Se ejecuta automáticamente cuando el contenedor mongo inicia por primera vez

db = db.getSiblingDB('cac_valleverde');

// --- Agricultores ---
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
    ]);
    print("✅ Agricultores insertados");
}

// --- Usuarios ---
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
    print("✅ Usuarios insertados");
}
