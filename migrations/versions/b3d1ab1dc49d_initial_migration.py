"""initial migration

Revision ID: b3d1ab1dc49d
Revises: 
Create Date: 2021-12-24 20:14:24.082229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3d1ab1dc49d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tmdb_id', sa.Integer(), nullable=True),
    sa.Column('imdb_id', sa.String(length=15), nullable=True),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('original_title', sa.Text(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('genres', sa.Text(), nullable=True),
    sa.Column('add_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('imdb_id')
    )
    op.create_index(op.f('ix_movies_tmdb_id'), 'movies', ['tmdb_id'], unique=True)
    op.create_table('popularmovies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tmdb_id', sa.Integer(), nullable=True),
    sa.Column('add_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_popularmovies_tmdb_id'), 'popularmovies', ['tmdb_id'], unique=True)
    op.create_table('top250movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tmdb_id', sa.Integer(), nullable=True),
    sa.Column('add_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_top250movies_tmdb_id'), 'top250movies', ['tmdb_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_top250movies_tmdb_id'), table_name='top250movies')
    op.drop_table('top250movies')
    op.drop_index(op.f('ix_popularmovies_tmdb_id'), table_name='popularmovies')
    op.drop_table('popularmovies')
    op.drop_index(op.f('ix_movies_tmdb_id'), table_name='movies')
    op.drop_table('movies')
    # ### end Alembic commands ###
