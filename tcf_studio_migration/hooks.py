import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    _migrate_brand_tag(env)
    _migrate_fragrance_uses(env)
    _migrate_product_purpose_category(env)
    _migrate_product_purpose(env)
    _migrate_brand_brand(env)
    _migrate_perfume_perfume(env)
    _migrate_brand_brand_tag_m2m(env)
    _migrate_product_template_fields(env)
    _migrate_sale_order_fields(env)
    _migrate_res_partner_bank_fields(env)
    _migrate_stock_picking_fields(env)
    _migrate_stock_move_line_fields(env)
    _migrate_mrp_production_fields(env)
    _migrate_product_template_purpose_m2m(env)


def _migrate_brand_tag(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO brand_tag (id, name, color, create_date, create_uid, write_date, write_uid)
                SELECT id, x_name, x_color, create_date, create_uid, write_date, write_uid
                FROM x_brand_tag
                ON CONFLICT (id) DO NOTHING
            """)
            env.cr.execute("""
                SELECT setval('brand_tag_id_seq', COALESCE((SELECT MAX(id) FROM brand_tag), 1))
            """)
            _logger.info('brand_tag migration completed.')
    except Exception as e:
        _logger.warning('brand_tag migration skipped: %s', e)


def _migrate_fragrance_uses(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO fragrance_uses (id, name, sequence, create_date, create_uid, write_date, write_uid)
                SELECT id, x_name, x_studio_sequence, create_date, create_uid, write_date, write_uid
                FROM x_fragrance_uses
                ON CONFLICT (id) DO NOTHING
            """)
            env.cr.execute("""
                SELECT setval('fragrance_uses_id_seq', COALESCE((SELECT MAX(id) FROM fragrance_uses), 1))
            """)
            _logger.info('fragrance_uses migration completed.')
    except Exception as e:
        _logger.warning('fragrance_uses migration skipped: %s', e)


def _migrate_product_purpose_category(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO product_purpose_category (id, name, active, image_128, notes, sequence, create_date, create_uid, write_date, write_uid)
                SELECT id, x_name, x_active, x_studio_image, x_studio_notes, x_studio_sequence, create_date, create_uid, write_date, write_uid
                FROM x_product_purpose_cate
                ON CONFLICT (id) DO NOTHING
            """)
            env.cr.execute("""
                SELECT setval('product_purpose_category_id_seq', COALESCE((SELECT MAX(id) FROM product_purpose_category), 1))
            """)
            _logger.info('product_purpose_category migration completed.')
    except Exception as e:
        _logger.warning('product_purpose_category migration skipped: %s', e)


def _migrate_product_purpose(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO product_purpose (id, name, active, color, image_128, notes, sequence, category_id, create_date, create_uid, write_date, write_uid)
                SELECT id, x_name, x_active, x_color, x_studio_image, x_studio_notes, x_studio_sequence,
                       "x_studio_many2one_field_fPAvQ",
                       create_date, create_uid, write_date, write_uid
                FROM x_product_purposes
                ON CONFLICT (id) DO NOTHING
            """)
            env.cr.execute("""
                SELECT setval('product_purpose_id_seq', COALESCE((SELECT MAX(id) FROM product_purpose), 1))
            """)
            _logger.info('product_purpose migration completed.')
    except Exception as e:
        _logger.warning('product_purpose migration skipped: %s', e)


def _migrate_brand_brand(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO brand_brand (id, name, active, code, notes, sequence, pipeline_status, create_date, create_uid, write_date, write_uid)
                SELECT id, x_name, x_active, x_studio_code, x_studio_notes, x_studio_sequence,
                       "x_studio_selection_field_URXGd",
                       create_date, create_uid, write_date, write_uid
                FROM x_brand
                ON CONFLICT (id) DO NOTHING
            """)
            env.cr.execute("""
                SELECT setval('brand_brand_id_seq', COALESCE((SELECT MAX(id) FROM brand_brand), 1))
            """)
            _logger.info('brand_brand migration completed.')
    except Exception as e:
        _logger.warning('brand_brand migration skipped: %s', e)


def _migrate_perfume_perfume(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO perfume_perfume (id, name, active, avatar_image, code, brand_id, notes, priority, sequence, status, create_date, create_uid, write_date, write_uid)
                SELECT id, x_name, x_active, x_avatar_image, x_studio_code,
                       "x_studio_many2one_field_bbUKk",
                       x_studio_notes, x_studio_priority_1, x_studio_sequence, x_studio_status,
                       create_date, create_uid, write_date, write_uid
                FROM x_perfumes
                ON CONFLICT (id) DO NOTHING
            """)
            env.cr.execute("""
                SELECT setval('perfume_perfume_id_seq', COALESCE((SELECT MAX(id) FROM perfume_perfume), 1))
            """)
            _logger.info('perfume_perfume migration completed.')
    except Exception as e:
        _logger.warning('perfume_perfume migration skipped: %s', e)


def _migrate_brand_brand_tag_m2m(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO brand_brand_brand_tag_rel (brand_brand_id, brand_tag_id)
                SELECT x_brand_id, x_brand_tag_id
                FROM x_brand_x_brand_tag_rel
                ON CONFLICT DO NOTHING
            """)
            _logger.info('brand_brand_brand_tag_rel m2m migration completed.')
    except Exception as e:
        _logger.warning('brand_brand_brand_tag_rel m2m migration skipped: %s', e)


def _migrate_product_template_purpose_m2m(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                INSERT INTO product_template_product_purpose_rel (product_template_id, product_purpose_id)
                SELECT product_template_id, x_product_purposes_id
                FROM product_template_x_product_purposes_rel
                ON CONFLICT DO NOTHING
            """)
            _logger.info('product_template_product_purpose_rel m2m migration completed.')
    except Exception as e:
        _logger.warning('product_template_product_purpose_rel m2m migration skipped: %s', e)


def _migrate_product_template_fields(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                UPDATE product_template SET
                    fragrance_use_id = "x_Uses_Of_Perfume",
                    admin_key = x_studio_admin_key,
                    alternative_code = x_studio_alternative_code,
                    brand_company = x_studio_brand_company,
                    cas_number = x_studio_cas_number,
                    common_code = x_studio_common_code,
                    common_name = x_studio_common_name,
                    fcost = x_studio_cost,
                    scrap_arabic_name = x_studio_scrap_arabic_name,
                    scrap_name = x_studio_scrap_name,
                    scrapped = x_studio_scrapped,
                    kg_price = x_kg_price
                WHERE id IN (SELECT id FROM product_template)
            """)
            _logger.info('product_template fields migration completed.')
    except Exception as e:
        _logger.warning('product_template fields migration skipped: %s', e)

    try:
        with env.cr.savepoint():
            env.cr.execute("""
                UPDATE product_template SET fcost_monetary = x_studio_cost0
                WHERE x_studio_cost0 IS NOT NULL
            """)
            _logger.info('product_template fcost_monetary migration completed.')
    except Exception as e:
        _logger.warning('product_template fcost_monetary migration skipped: %s', e)


def _migrate_sale_order_fields(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                UPDATE sale_order SET
                    account_name = x_studio_account_name,
                    bank_account_id = x_studio_bank_account,
                    bank_account_currency_id = x_studio_bank_account_currency,
                    branch_code = x_studio_branch_code,
                    iban_number = x_studio_iban_number,
                    swift_code = x_studio_swift_code
                WHERE id IN (SELECT id FROM sale_order)
            """)
            _logger.info('sale_order fields migration completed.')
    except Exception as e:
        _logger.warning('sale_order fields migration skipped: %s', e)


def _migrate_res_partner_bank_fields(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                UPDATE res_partner_bank SET
                    branch_code = x_studio_branch_code,
                    iban_number = x_studio_iban_number
                WHERE id IN (SELECT id FROM res_partner_bank)
            """)
            _logger.info('res_partner_bank fields migration completed.')
    except Exception as e:
        _logger.warning('res_partner_bank fields migration skipped: %s', e)


def _migrate_stock_picking_fields(env):
    # These fields are now derived from the linked Manufacturing Order.  Do
    # not copy the legacy Studio snapshot over the computed source of truth.
    _logger.info(
        'stock_picking MO info migration skipped: values are derived from '
        'mrp_production_id.'
    )


def _migrate_stock_move_line_fields(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                UPDATE stock_move_line SET
                    special_code = x_studio_special_code,
                    special_code_1 = x_studio_special_code_1,
                    special_code_2 = x_studio_special_code_2
                WHERE id IN (SELECT id FROM stock_move_line)
            """)
            _logger.info('stock_move_line fields migration completed.')
    except Exception as e:
        _logger.warning('stock_move_line fields migration skipped: %s', e)


def _migrate_mrp_production_fields(env):
    try:
        with env.cr.savepoint():
            env.cr.execute("""
                UPDATE mrp_production SET
                    sale_order_id = x_studio_sales_order
                WHERE id IN (SELECT id FROM mrp_production)
            """)
            _logger.info('mrp_production fields migration completed.')
    except Exception as e:
        _logger.warning('mrp_production fields migration skipped: %s', e)
