import type { Struct, Schema } from '@strapi/strapi';

export interface SeoMetaData extends Struct.ComponentSchema {
  collectionName: 'components_seo_meta_data';
  info: {
    displayName: 'Meta Data';
  };
  attributes: {
    metaTitle: Schema.Attribute.String;
    metaDescription: Schema.Attribute.Text;
    metaImage: Schema.Attribute.Media<'images' | 'files'>;
  };
}

declare module '@strapi/strapi' {
  export module Public {
    export interface ComponentSchemas {
      'seo.meta-data': SeoMetaData;
    }
  }
}
