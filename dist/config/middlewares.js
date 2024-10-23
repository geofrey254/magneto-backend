module.exports = [
    // Required middlewares
    "strapi::errors",
    "strapi::security",
    "strapi::cors", // CORS middleware
    {
        name: "strapi::cors",
        config: {
            origin: ["http://localhost:3000"], // Your Next.js URL
            methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            // You can add more CORS options as needed
        },
    },
    "strapi::logger",
    "strapi::poweredBy",
    "strapi::query",
    "strapi::body",
    "strapi::session",
    "strapi::favicon",
    "strapi::public",
];
