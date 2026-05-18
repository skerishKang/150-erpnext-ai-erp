// Padiem AI Dashboard — Custom Page skeleton
// Actual implementation comes in a later PR.

frappe.pages["padiem-dashboard"].on_page_load = function (wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "Padiem AI ERP",
        single_column: true,
    });

    $(wrapper).find(".layout-main").html(`
        <div class="padiem-dashboard" style="padding: 20px;">
            <h2>Padiem AI ERP — CEO Dashboard</h2>
            <p>Dashboard skeleton — AI integration pending.</p>
        </div>
    `);
};
